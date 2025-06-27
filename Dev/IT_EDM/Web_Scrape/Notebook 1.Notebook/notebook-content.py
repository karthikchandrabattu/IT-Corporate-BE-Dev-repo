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
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace

# 1. Create Spark session (Fabric notebooks already have `spark`)
spark = SparkSession.builder.getOrCreate()

# 2A. If your source is Parquet (preferred), simply:
raw_df = spark.read.parquet("abfss://eb87c50a-8bc7-40f8-bb1a-8a135398c6f4@onelake.dfs.fabric.microsoft.com/89412544-9ac3-4f39-a42d-09c035b68d13/Files/Pricing/20-05-2025/z7183_findchips_2025-05-20_part_3.parquet")


raw_df.printSchema()
raw_df.show(5, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace

# 1. Create Spark session (Fabric notebooks already have `spark`)
spark = SparkSession.builder.getOrCreate()

# 2A. If your source is Parquet (preferred), simply:
raw_df = spark.read.parquet("abfss://eb87c50a-8bc7-40f8-bb1a-8a135398c6f4@onelake.dfs.fabric.microsoft.com/89412544-9ac3-4f39-a42d-09c035b68d13/Files/Pricing/20-05-2025/z7183_findchips_2025-05-20_part_3.parquet")


raw_df.printSchema()
raw_df.show(5, truncate=False)

from pyspark.sql.functions import when, lit

string_cols = [f.name for f in raw_df.schema.fields if f.dataType.simpleString() == "string"]

df_clean = raw_df
for c in string_cols:
    # 4A. Remove backslashes and forward slashes entirely:
    df_clean = df_clean.withColumn(c,
        regexp_replace(col(c), r"[\\/]", "")
    )
    # 4B. Replace consecutive double quotes or single quotes with a single character:
    df_clean = df_clean.withColumn(c,
        regexp_replace(col(c), r"\"{2,}", "\"")   # turn """" -> "
    )
    df_clean = df_clean.withColumn(c,
        regexp_replace(col(c), r"'{2,}", "'")    # turn '''' -> '
    )
    # 4C. (Optional) If you want to strip any other weird punctuation, you can add more rules,
    #      e.g. remove question marks except if they are meaningful:
    df_clean = df_clean.withColumn(c,
        regexp_replace(col(c), r"[?]{2,}", "?")  # collapse multiple "?" to single "?"
    )

# 5. Handle nulls if needed. For example, if you want to convert empty strings to NULL:
df_clean = df_clean.replace("", None)   # turns any zero‐length string into a true null

# 6. Re-inspect a few rows:
df_clean.show(5, truncate=False)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
