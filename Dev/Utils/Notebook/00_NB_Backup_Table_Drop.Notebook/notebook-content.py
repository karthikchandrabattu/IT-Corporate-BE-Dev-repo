# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "89412544-9ac3-4f39-a42d-09c035b68d13",
# META       "default_lakehouse_name": "DE_LH_Bronze",
# META       "default_lakehouse_workspace_id": "eb87c50a-8bc7-40f8-bb1a-8a135398c6f4",
# META       "known_lakehouses": [
# META         {
# META           "id": "89412544-9ac3-4f39-a42d-09c035b68d13"
# META         },
# META         {
# META           "id": "16fadab9-4226-43b4-885a-6f54f0951826"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # This Notebook Drops the Backup Tables from the Bronze and Silver Layer


# CELL ********************

import com.microsoft.spark.fabric
from com.microsoft.spark.fabric.Constants import Constants

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

meta_conn = "WH_DE_MetaData"
meta_schema = "dbo"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

query = "SELECT DISTINCT TABLE_NAME, TABLE_SCHEMA FROM DE_LH_Bronze.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME LIKE '%_backup_%'"

df = spark.read.option(Constants.DatabaseName, "DE_LH_Bronze").synapsesql(query)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

try:
    for row in df.collect():
        table_name = row["TABLE_NAME"]
        table_schema = row["TABLE_SCHEMA"]
        drop_query = f"DROP TABLE {table_schema}.{table_name}"
        spark.sql(drop_query)
    print("Drop Table was Completed")
except Exception as e:
    print(e)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### DROP Silver Backup Tables

# CELL ********************

query = "SELECT DISTINCT TABLE_NAME, TABLE_SCHEMA FROM DE_LH_Silver.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME LIKE '%_backup_%'"

df = spark.read.option(Constants.DatabaseName, "DE_LH_Bronze").synapsesql(query)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

try:
    for row in df.collect():
        table_name = row["TABLE_NAME"]
        table_schema = row["TABLE_SCHEMA"]
        drop_query = f"DROP TABLE DE_LH_Silver.{table_schema}.{table_name}"
        try:
            spark.sql(drop_query)
        except Exception as e:
            print(e)
    print("Drop Table was Completed")
except Exception as e:
    print(e)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

mssparkutils.notebook.exit("Success")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## mssparkutils.notebook.exit("Success")
