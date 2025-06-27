# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from com.microsoft.spark.fabric import Constants
import com.microsoft.spark.fabric
from com.microsoft.spark.fabric.Constants import Constants 
from pyspark.sql.functions import current_timestamp

from delta.tables import DeltaTable
import pandas as pd
import traceback
import json
import time
import requests
import sempy.fabric as fabric

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# PARAMETERS CELL ********************

table_list = "Sales, Visit, Roster"
batch_id = -1

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

list_of_tables = table_list.split(',')
count_of_tables = len(list_of_tables)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


from datetime import datetime, timezone
from zoneinfo import ZoneInfo     

current_time_utc = datetime.now(timezone.utc)      
current_time = current_time_utc.astimezone(ZoneInfo("America/Toronto"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Mail Content

# CELL ********************

recipient_email = """Viswanath.Kolisetty@FutureElectronics.com"""
subject = "Fabric Pipeline Alert : Table Schema mismatch"
table_rows = ""

content = ["I hope this message finds you well. Unfortunately some of the tables during the process got some mismatched datatypes or Column names from the source.","these tables has mismatch in the source system so we stopped the process for these tables"]

message = f"""<div class="alert-box" style="border-left: 4px solid #dc2626; background-colour: #fee2e2;">
                <div calss="alert-icon>❌</div>
                <div calss="alert-text" style="color: red;">
                    <strong>Process Status: </strong> {count_of_tables} Tables stopped due t mismatch.
                </div>
                </div>"""

content = [
    "I hope this message finds you well. Unfortunately, during today's pipeline run some tables failed because the source definition no longer matches our target schema.",
    "These tables show mismatches in the source system, so the process was stopped for them."
]

alert_html = f"""
<div class="alert-box" style="border-left:4px solid #dc2626;background-color:#fee2e2;">
    <div class="alert-icon">❌</div>
    <div class="alert-text" style="color:#dc2626;">
        <strong>Process Status:</strong> {count_of_tables} tables stopped due to mismatch.
    </div>
</div>
"""

# 3️⃣  HTML body (full CSS kept, typos fixed, DIV hierarchy clean)
email_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Fabric Pipeline Notification</title>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

* {{ margin:0;padding:0;box-sizing:border-box; }}

body {{
  font-family:'Roboto',Arial,sans-serif;
  line-height:1.6;
  color:#1e293b;
  background-color:#f1f5f9;
  padding:20px;
}}

.email-container {{
  max-width:650px;margin:0 auto;background:#ffffff;
  border-radius:10px;overflow:hidden;
  box-shadow:0 4px 15px rgba(0,0,0,.12);
}}

.email-header {{
  background:#f1f5f9;padding:25px 40px;text-align:center;
  border-bottom-left-radius:30% 15%;border-bottom-right-radius:30% 15%;
}}

.company-logo {{
  max-height:100px;filter:drop-shadow(0 4px 6px rgba(0,0,0,.3));
  animation:logoFloat 6s ease-in-out infinite;
}}

.email-body {{ padding:35px; }}

.greeting {{ font-size:22px;font-weight:500;margin-bottom:20px; }}

.content {{ font-size:16px;margin-bottom:25px;line-height:1.7; }}

.batch-report-section {{ display:flex;gap:10px;margin-bottom:20px; }}

.chip {{ display:flex;background:#f0f0f0;border-radius:5px;overflow:hidden; }}
.chip-label  {{ padding:10px;background:#e0e0e0;font-weight:600;white-space:nowrap; }}
.chip-value  {{ padding:10px; }}

.alert-box {{
  padding:18px 20px;margin:25px 0;border-radius:6px;display:flex;align-items:center;
  box-shadow:0 2px 5px rgba(220,38,38,.15);animation:pulse 3s infinite;
}}
.alert-icon {{ margin-right:15px;font-size:24px; }}
.alert-text {{ font-weight:500; }}

.divider {{ height:1px;background:#cbd5e1;margin:30px 0; }}

.signature {{ margin-top:30px;font-size:15px;color:#475569; }}
.name {{ font-weight:600;color:#1e293b; }}

.email-footer {{
  background:#314569;padding:25px;text-align:center;border-top:1px solid #cbd5e1;
}}

@keyframes pulse {{ 0%{{transform:scale(1);}}50%{{transform:scale(1.02);}}100%{{transform:scale(1);}} }}
@keyframes logoFloat {{ 0%{{transform:translateY(0);}}50%{{transform:translateY(-6px);}}100%{{transform:translateY(0);}} }}

@media(max-width:600px){{
  body{{padding:10px;}}
  .email-body{{padding:25px 20px;}}
  .greeting{{font-size:20px;}}
  .batch-report-section{{flex-direction:column;}}
}}
</style>
</head>

<body>
  <div class="email-container">
    <!-- ▸ Header logo -->
    <div class="email-header">
      <img src="https://seekvectorlogo.com/wp-content/uploads/2020/11/future-electronics-vector-logo.png"
           alt="Future Electronics" class="company-logo">
    </div>

    <!-- ▸ Main body -->
    <div class="email-body">
      <div class="greeting">Hi&nbsp;Team,</div>

      <div class="content">{content[0]}</div>

      <!-- chips -->
      <div class="batch-report-section">
        <div class="chip">
          <div class="chip-label">Batch ID:</div>
          <div class="chip-value">{batch_id}</div>
        </div>
        <div class="chip">
          <div class="chip-label">Report&nbsp;Date:</div>
          <div class="chip-value">{current_time}</div>
        </div>
      </div>

      <!-- alert -->
      {alert_html}

      <div class="content">{table_list} – {content[1]}</div>

      <div class="divider"></div>

      <div class="content" style="font-style:italic;color:#ba1d1d;">
        This is a system-generated email. Please do not reply.
      </div>

      <div class="signature">
        <div class="name">Regards,</div>
         <div class="name">Viswanath K,</div>
        <div class="name">Microsoft Fabric Data Engineer</div>
        <div class="name">Future Electronics</div>
      </div>
    </div>

    <!-- ▸ Footer logo -->
    <div class="email-footer">
      <img src="https://miro.medium.com/v2/resize:fit:1000/1*7DUq1lvkZnByiqOHjLd_Zw.png"
           alt="Fabric Logo" style="max-height:60px;border-radius:25px;">
    </div>
  </div>
</body>
</html>"""

# 4️⃣  Ready-to-use output
print(email_body.strip())





# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import json

val = {
    "email_body": email_body,
    "recipient_email": recipient_email,
    "subject": subject
}
json_str = json.dumps(val)
mssparkutils.notebook.exit(json_str)
print(val)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
