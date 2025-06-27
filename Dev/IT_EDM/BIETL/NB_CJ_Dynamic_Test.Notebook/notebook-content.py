# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "9fce3718-5576-493d-a599-d7dc0f7a0e3c",
# META       "default_lakehouse_name": "LH_SQL_BIETL",
# META       "default_lakehouse_workspace_id": "eb87c50a-8bc7-40f8-bb1a-8a135398c6f4",
# META       "known_lakehouses": [
# META         {
# META           "id": "59c51572-3230-4edc-9c45-084cfac270d4"
# META         },
# META         {
# META           "id": "9fce3718-5576-493d-a599-d7dc0f7a0e3c"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

import requests
import json
import base64
import time
from datetime import datetime, timedelta
from notebookutils import mssparkutils

# ───────────────────────────────────────────────────────────────────────────────
# 1) TOKEN HELPERS: fetch & refresh Fabric REST AAD token
# ───────────────────────────────────────────────────────────────────────────────

def get_access_token():
    """
    Uses mssparkutils.credentials.getToken('pbi') to fetch a Fabric-compatible JWT.
    We decode its payload to extract 'exp' so we know when to refresh.
    """
    token_jwt = mssparkutils.credentials.getToken('pbi')
    header, payload, signature = token_jwt.split('.')
    padded  = payload + "=" * ((4 - len(payload) % 4) % 4)
    decoded = base64.b64decode(padded)
    info    = json.loads(decoded)
    if 'exp' not in info:
        raise ValueError("Token payload missing 'exp'")
    exp_ts = info['exp']
    return token_jwt, datetime.utcfromtimestamp(exp_ts)

access_token, token_expiry = get_access_token()

def get_valid_access_token():
    """
    Returns a non-expired Fabric REST bearer token. If it's within 5 minutes of expiry,
    retrieves a fresh one via get_access_token().
    """
    global access_token, token_expiry
    if datetime.utcnow() >= (token_expiry - timedelta(minutes=5)):
        access_token, token_expiry = get_access_token()
    return access_token

# ───────────────────────────────────────────────────────────────────────────────
# 2) CONFIGURATION: set your workspaceId, connection IDs, etc.
# ───────────────────────────────────────────────────────────────────────────────

workspace_id          = "eb87c50a-8bc7-40f8-bb1a-8a135398c6f4"           # e.g. "eb87c50a-8bc7-40f8-bb1a-8a135398c6f4"
azure_sql_connection  = "d1565b37-5a8c-4ebb-9b25-ed365e944970"  # e.g. "d1565b37-5a8c-4ebb-9b25-ed365e944970"
lakehouse_artifact_id = "59c51572-3230-4edc-9c45-084cfac270d4"   # e.g. "59c51572-3230-4edc-9c45-084cfac270d4"

# ───────────────────────────────────────────────────────────────────────────────
# 3) BUILD THE “PUBLIC” JSON (ContentDetails) FOR A NEW COPY JOB
# ───────────────────────────────────────────────────────────────────────────────

# We’ll create a Copy Job that does a straight SELECT * from logs.ETL_Status_Table
# into a Lakehouse table named logs_ETL_Status_Table. You can adjust schema/table names.

copy_job_content = {
    "properties": {
        "jobMode": "Batch",
        "source": {
            "type": "AzureSqlTable",
            "connectionSettings": {
                "type": "AzureSqlDatabase",
                "typeProperties": {
                    "database": "EDM"
                },
                "externalReferences": {
                    "connection": azure_sql_connection
                }
            }
        },
        "destination": {
            "type": "LakehouseTable",
            "connectionSettings": {
                "type": "Lakehouse",
                "typeProperties": {
                    "workspaceId": workspace_id,
                    "artifactId": lakehouse_artifact_id,
                    "rootFolder": "Tables"
                }
            }
        },
        "policy": {
            "timeout": "0.12:00:00"
        }
    },
    "activities": [
        {
            "id": "d7003fb8-d341-41cc-a2d1-5c38faa15894",
            "properties": {
                "source": {
                    "datasetSettings": {
                        "schema": "logs",
                        "table": "ETL_Status_Table"
                    },
                    "partitionOption": "None"
                },
                "destination": {
                    "datasetSettings": {
                        "table": "logs_ETL_Status_Table"
                    },
                    "writeBehavior": "Append"
                },
                "enableStaging": False
                # Omitting translator.mappings means "copy all columns"
            }
        }
    ]
}

# ───────────────────────────────────────────────────────────────────────────────
# 4) WRAP INTO THE TOP-LEVEL “CREATE COPY JOB” PAYLOAD
# ───────────────────────────────────────────────────────────────────────────────

create_body = {
    "displayName": "CJ_SQL_BIETL_LH_WH_AutoAPI",   # Choose any unique name
    "description": "Created programmatically via Public API",
    "definition": {
        "path": "/",
        "payloadType": "Public",
        "payload": json.dumps(copy_job_content)
    }
}

# ───────────────────────────────────────────────────────────────────────────────
# 5) CALL POST /copyJobs TO CREATE THE NEW JOB
# ───────────────────────────────────────────────────────────────────────────────

token = get_valid_access_token()
create_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/copyJobs"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

resp = requests.post(create_url, headers=headers, data=json.dumps(create_body))
if resp.status_code not in (200, 201, 202):
    raise RuntimeError(f"Failed to create Copy Job (HTTP {resp.status_code}):\n{resp.text}")

new_copyjob_id = resp.json().get("id") or resp.json().get("objectId") or resp.json().get("copyJobId")
print(f"✅ Copy Job created. New GUID = {new_copyjob_id}")

# ───────────────────────────────────────────────────────────────────────────────
# 6) TRIGGER THE NEW COPY JOB RUN
# ───────────────────────────────────────────────────────────────────────────────

run_url = (
    f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}"
    f"/copyJobs/{new_copyjob_id}/jobs/instances?jobType=CopyJob"
)

run_resp = requests.post(
    run_url,
    headers={"Authorization": f"Bearer {get_valid_access_token()}"},
    json={}
)
if run_resp.status_code != 202:
    print(f"⚠️ Created Copy Job but failed to trigger (HTTP {run_resp.status_code}):\n{run_resp.text}")
else:
    run_id = run_resp.headers["Location"].rstrip("/").split("/")[-1]
    print(f"✅ Copy Job triggered. runId = {run_id}")

    # ─────────────────────────────────────────────────────────────────────────────
    # 7) POLL RUN STATUS UNTIL TERMINAL                                         

    def get_status(ws_id, cj_id, r_id):
        t = get_valid_access_token()
        status_url = (
            f"https://api.fabric.microsoft.com/v1/workspaces/{ws_id}"
            f"/items/{cj_id}/jobs/instances/{r_id}?jobType=CopyJob"
        )
        r = requests.get(status_url, headers={"Authorization": f"Bearer {t}"})
        if r.status_code == 200:
            return r.json().get("status", "Unknown")
        return f"Error({r.status_code})"

    while True:
        current_status = get_status(workspace_id, new_copyjob_id, run_id)
        if current_status in ("Succeeded", "Failed", "Cancelled", "Completed"):
            print(f"Final status = {current_status}")
            break
        print(f"Status = {current_status}. Sleeping 10s…")
        time.sleep(10)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
