# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "c7351b11-b8bf-4a4d-8980-c4d5629c85c4",
# META       "default_lakehouse_name": "BISQL_EDM",
# META       "default_lakehouse_workspace_id": "0d16db09-7d7e-43e0-991f-2049ff0141c6",
# META       "known_lakehouses": [
# META         {
# META           "id": "c7351b11-b8bf-4a4d-8980-c4d5629c85c4"
# META         },
# META         {
# META           "id": "c20fa2e2-76c7-446a-9db7-9623b99fc1df"
# META         },
# META         {
# META           "id": "9fce3718-5576-493d-a599-d7dc0f7a0e3c"
# META         }
# META       ]
# META     },
# META     "environment": {}
# META   }
# META }

# CELL ********************

from pyspark.sql.functions import col, lit
from delta.tables import DeltaTable
from notebookutils import runtime
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import re, pytz, queue, threading

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# PARAMETERS CELL ********************

SourceSystem = "SQLBIETL"
TableListID = "all"
DWBatchID = 99999
Description = "Bronze to Silver Layer Load"
ActivityName = "LoadSilverTables"
MAX_THREADS = 10

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


meta_path = "abfss://0d16db09-7d7e-43e0-991f-2049ff0141c6@onelake.dfs.fabric.microsoft.com/7492ec90-0f87-488e-b8d0-45234b899b33/Tables/dbo/Metadata_TableList"
audit_log_path = "abfss://0d16db09-7d7e-43e0-991f-2049ff0141c6@onelake.dfs.fabric.microsoft.com/c7351b11-b8bf-4a4d-8980-c4d5629c85c4/Tables/audit_log_staging"
lakehouse_base_path = "abfss://eb87c50a-8bc7-40f8-bb1a-8a135398c6f4@onelake.dfs.fabric.microsoft.com/9fce3718-5576-493d-a599-d7dc0f7a0e3c/Tables/"
#abfss://f3415686-9475-4b7d-b095-1015b73eb6e7@onelake.dfs.fabric.microsoft.com/3596aaeb-e1c5-428b-903b-cfcfd23cffb9/Tables
output_base = "abfss://f3415686-9475-4b7d-b095-1015b73eb6e7@onelake.dfs.fabric.microsoft.com/3596aaeb-e1c5-428b-903b-cfcfd23cffb9/Tables/"



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


est = pytz.timezone("US/Eastern")
today_date_str = datetime.now(est).strftime("%Y-%m-%d")
PipelineID = runtime.context.get("currentNotebookName")
RunID = mssparkutils.env.getJobId()
ProcessDate = datetime.now(est).date()


errorQueue = queue.Queue()
lock = threading.Lock()
processed_tables = set()


def clean_column_name_upper(name):
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^\w]", "_", name)
    return name.upper()


dbo_meta_data_tablelist = spark.read.format("delta").load(meta_path)

if TableListID.lower() == 'all':
    TableListDF = dbo_meta_data_tablelist.filter(
        (col("SourceSystemName") == SourceSystem) & (col("IsActive") == True)
    )
else:
    TableListDF = dbo_meta_data_tablelist.filter(
        (col("ID").cast("string").isin(TableListID.split(","))) &
        (col("SourceSystemName") == SourceSystem) & (col("IsActive") == True)
    )

table_id_map = TableListDF.select("SourceTableName", "ID") \
    .toPandas().set_index("SourceTableName")["ID"].to_dict()

TableList = list(table_id_map.keys())

if DeltaTable.isDeltaTable(spark, audit_log_path):
    DeltaTable.forPath(spark, audit_log_path).delete()


def main(table, errorQueue):
    with lock:
        if table in processed_tables:
            return
        processed_tables.add(table)

    input_path = f"{input_base}/{today_date_str}/{table}"
    output_path = f"{output_base}{table.upper()}"
    start_time = datetime.now(est)

    try:
        df = spark.read.format("delta").load(f"{lakehouse_base_path}/{table}")
        df_clean = df.select([col(c).alias(clean_column_name_upper(c)) for c in df.columns]).cache()
        stage_count = df_clean.count()

        df_clean.write.format("delta") \
            .mode("overwrite") \
            .option("mergeSchema", "true") \
            .save(output_path)

        end_time = datetime.now(est)

        log_data = [{
            "ETLBatchID": DWBatchID,
            "PipelineID": PipelineID,
            "RunID": RunID,
            "BatchName": table,
            "ActivityName": ActivityName,
            "ProcessDate": ProcessDate,
            "BatchStart": start_time,
            "BatchEnd": end_time,
            "StartTime": start_time,
            "EndTime": end_time,
            "Status": 1,
            "SystemErrorMessage": "",
            "SourceCount": stage_count,
            "StageCount": stage_count,
            "ListType": "Default",
            "ListID": int(table_id_map.get(table, 0)),
            "FileWrittenToLakehouse": output_path,
            "CopyingDuration": str((end_time - start_time).seconds),
            "DataReadSize": str(df.rdd.map(lambda row: len(str(row))).sum()),
            "DataWriteSize": str(df_clean.rdd.map(lambda row: len(str(row))).sum()),
            "ThroughputValue": round(stage_count / ((end_time - start_time).seconds + 1), 2),
            "Description": Description
        }]

    except Exception as e:
        end_time = datetime.now(est)
        log_data = [{
            "ETLBatchID": DWBatchID,
            "PipelineID": PipelineID,
            "RunID": RunID,
            "BatchName": table,
            "ActivityName": ActivityName,
            "ProcessDate": ProcessDate,
            "BatchStart": start_time,
            "BatchEnd": end_time,
            "StartTime": start_time,
            "EndTime": end_time,
            "Status": 2,
            "SystemErrorMessage": str(e),
            "SourceCount": 0,
            "StageCount": 0,
            "ListType": "Default",
            "ListID": int(table_id_map.get(table, 0)),
            "FileWrittenToLakehouse": output_path,
            "CopyingDuration": str((end_time - start_time).seconds),
            "DataReadSize": "0",
            "DataWriteSize": "0",
            "ThroughputValue": 0.0,
            "Description": Description
        }]
        errorQueue.put(e)

    log_df = spark.createDataFrame(log_data)
    log_df.write.format("delta").mode("append").save(audit_log_path)
    print(f"Logged: {table}")

def threaded_run(table):
    try:
        main(table, errorQueue)
    except Exception as e:
        errorQueue.put(e)

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = [executor.submit(threaded_run, tbl) for tbl in TableList]
    for future in as_completed(futures):
        _ = future.result()

if not errorQueue.empty():
    ex = errorQueue.get()
    errorQueue.task_done()
    raise Exception(ex)

print("All tables processed and audit log updated.")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
