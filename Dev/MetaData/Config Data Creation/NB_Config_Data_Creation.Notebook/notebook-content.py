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
from pyspark.sql.functions import col
from pyspark.sql.types import StringType

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

query = "SELECT * FROM [WH_DE_MetaData].[Config].[SQLServerSourceInformationSchema]"
meta_df = spark.read.option(Constants.DatabaseName, "WH_DE_MetaData").synapsesql(query)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

meta_df.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ──────────────────────────────────────────────────────────────
# Build a 4-column DataFrame
#   1. TABLE_NAME
#   2. TABLE_SCHEMA
#   3. SELECT_STATEMENT  (e.g.  SELECT CAST(Mfr AS VARCHAR) AS Mfr …)
#   4. PRIMARY_KEY
# Works in Microsoft Fabric or any Spark runtime with
# INFORMATION_SCHEMA.COLUMNS + KEY_COLUMN_USAGE.
# ──────────────────────────────────────────────────────────────
from pyspark.sql import functions as F


# 2️⃣  SQL-Server → Fabric type map ------------------------------
type_map = {
    "char":      "VARCHAR",
    "varchar":   "VARCHAR",
    "nvarchar":  "VARCHAR",
    "bit":       "BIT",
    "tinyint":   "INT",
    "smallint":  "INT",
    "int":       "INT",
    "bigint":    "BIGINT",
    "numeric":   "DECIMAL(18,2)",
    "decimal":   "DECIMAL(18,2)",
    "float":     "DECIMAL(18,2)",
    "datetime":  "DATETIME2",
    "date":      "DATE"
}

case_expr = "CASE " + " ".join(
    [f"WHEN DATA_TYPE = '{src}' THEN '{tgt}'" for src, tgt in type_map.items()]
) + " END"

# 3️⃣  Per-table SELECT list (no duplicate column name!) ----------
cols_with_cast = (
    meta_df
    .withColumn(
        "column_expr",
        F.concat(
            F.lit("CAST(["),
            F.col("COLUMN_NAME"),
            F.lit("] AS "),
            F.expr(case_expr),
            F.lit(") AS ["),
            F.regexp_replace(F.col("COLUMN_NAME"), r"\s+", "_"),
            F.lit("]")
        )
    )
    .groupBy("TABLE_SCHEMA", "TABLE_NAME")
    .agg(F.concat_ws(", ", F.collect_list("column_expr")).alias("SELECT_LIST"))
)

# 4️⃣  Primary-key list ------------------------------------------
pk_cols = (
    meta_df.groupBy("TABLE_SCHEMA", "TABLE_NAME")
         .agg(F.concat_ws(", ", F.collect_list(F.regexp_replace(F.col("COLUMN_NAME"), r"\s+", "_"))).alias("PRIMARY_KEY"))
)

# 5️⃣  Final dataframe -------------------------------------------
result_df = (
    cols_with_cast
    .join(pk_cols, ["TABLE_SCHEMA", "TABLE_NAME"], "left")
    .withColumn(
        "SELECT_STATEMENT",
        F.concat(
            F.lit("SELECT "),
            F.col("SELECT_LIST"),
            F.lit(" FROM "),
            F.col("TABLE_SCHEMA"), F.lit("."), F.col("TABLE_NAME")
        )
    )
    .select(
        "TABLE_NAME",
        "TABLE_SCHEMA",
        "SELECT_STATEMENT",
        "PRIMARY_KEY"
    )
    .orderBy("TABLE_SCHEMA", "TABLE_NAME")
)

# 6️⃣  Preview ----------------------------------------------------
display(result_df)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

result_df.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# ───────────────────────────────
# 1️⃣  Add the running ConfigId
# ───────────────────────────────
w = Window.orderBy("TABLE_SCHEMA", "TABLE_NAME")      # any stable order is fine
enriched_df = result_df.withColumn("ConfigId", F.row_number().over(w))

# ───────────────────────────────
# 2️⃣  Derive / add the requested columns
# ───────────────────────────────
final_df = (
    enriched_df
    # literals
    .withColumn("DBSourceName",    F.lit("SQLBIETL"))
    .withColumn("SourceDBName",    F.lit("EDM"))
    .withColumn("IsFullLoad",      F.lit(1))
    .withColumn("IsActive",        F.lit(1))
    .withColumn("SourceSystem",    F.lit("SQL Server"))
    # direct mappings
    .withColumn("SourceSchemaName", F.col("TABLE_SCHEMA"))
    .withColumn("SourceTableName",  F.col("TABLE_NAME"))
    .withColumn("PrimaryKey",       F.col("PRIMARY_KEY"))
    .withColumn("SourceQuery",      F.col("SELECT_STATEMENT"))
    # Bronze / Silver / Gold names
    .withColumn("BronzeSchemaName", F.concat(F.lit("EDM_"), F.col("TABLE_SCHEMA")))
    .withColumn("BronzeTableName",  F.col("TABLE_NAME"))
    .withColumn("SilverSchemaName", F.concat(F.lit("EDM_"), F.col("TABLE_SCHEMA")))
    .withColumn("SilverTableName",  F.col("TABLE_NAME"))
    .withColumn("GoldSchemaName",   F.concat(F.lit("EDM_"), F.col("TABLE_SCHEMA")))
    .withColumn("GoldTableName",    F.col("TABLE_NAME"))
    # watermark placeholders (NULLs)
    .withColumn("WaterMarkField",  F.lit(None).cast("string"))
    .withColumn("WaterMarkValue",  F.lit(None).cast("string"))
    # select columns in the exact order you asked for
    .select(
        "ConfigId",
        "DBSourceName",
        "SourceDBName",
        "SourceSchemaName",
        "SourceTableName",
        "BronzeSchemaName",
        "BronzeTableName",
        "SilverSchemaName",
        "SilverTableName",
        "GoldSchemaName",
        "GoldTableName",
        "PrimaryKey",
        "IsFullLoad",
        "WaterMarkField",
        "WaterMarkValue",
        "IsActive",
        "SourceQuery",
        "SourceSystem"
    )
)

# ───────────────────────────────
# 3️⃣  Preview or write
# ───────────────────────────────
display(final_df)
# final_df.write.mode("overwrite").saveAsTable("dbo.ingestion_config")
final_df.write.mode("overwrite").synapsesql("WH_DE_MetaData.Config.OneTimeConfigETL")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import pandas as pd
# Load data into pandas DataFrame from f"{notebookutils.nbResPath}/builtin/meta.csv"
df = pd.read_csv(f"{notebookutils.nbResPath}/builtin/meta.csv")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.createDataFrame(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = df.withColumn("WaterMarkValue", col("WaterMarkValue").cast(StringType()))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.write.mode("append").synapsesql("WH_DE_MetaData.Config.MetaETL")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import pandas as pd
# Load data into pandas DataFrame from f"{notebookutils.nbResPath}/builtin/sourceinformationschema.csv"
df = pd.read_csv(f"{notebookutils.nbResPath}/builtin/sourceinformationschema.csv")
# display(df)
df=spark.createDataFrame(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.write.mode("append").synapsesql("WH_DE_MetaData.Config.SQLServerSourceInformationSchema")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
