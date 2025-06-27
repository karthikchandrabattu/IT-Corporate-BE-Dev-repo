# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "a82c5ac8-8053-43dd-9731-33e4b08cce04",
# META       "default_lakehouse_name": "LH_Test",
# META       "default_lakehouse_workspace_id": "eb87c50a-8bc7-40f8-bb1a-8a135398c6f4",
# META       "known_lakehouses": [
# META         {
# META           "id": "a82c5ac8-8053-43dd-9731-33e4b08cce04"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

df=spark.read.format('csv').option('header',True).load('abfss://eb87c50a-8bc7-40f8-bb1a-8a135398c6f4@onelake.dfs.fabric.microsoft.com/a82c5ac8-8053-43dd-9731-33e4b08cce04/Files/leads.csv')

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

df_cleansed=df.filter(df.email.isNotNull())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import *

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_refined=df.withColumn('phone_cleansed',regexp_replace(col("phone"),"[^0-9]",""))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_refined)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_date=df.withColumn('signup_date_refined',to_date(col(sign)))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import re

def clean_phone_number(phone):
    phone = str(phone).lower()
    
    # Remove anything after extension indicators (x, ext, #)
    phone = re.split(r'x|ext|#', phone)[0]
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Return last 10 digits if length is at least 10
    return digits[-10:] if len(digits) >= 10 else None


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType
import re


def clean_phone_number(phone):
    phone = str(phone).lower()
    phone = re.split(r'x|ext|#', phone)[0]
    digits = re.sub(r'\D', '', phone)
    return digits[-10:] if len(digits) >= 10 else None

clean_phone_udf = udf(clean_phone_number, StringType())
df = df.withColumn("cleaned_phone", clean_phone_udf(col("phone")))


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

import pandas as pd

wrangler_sample_df = pd.read_csv("https://aka.ms/wrangler/titanic.csv")
display(wrangler_sample_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "editable": false
# META }

# CELL ********************

import pandas as pd

wrangler_sample_df = pd.read_delta("abfss://eb87c50a-8bc7-40f8-bb1a-8a135398c6f4@onelake.dfs.fabric.microsoft.com/a82c5ac8-8053-43dd-9731-33e4b08cce04/Files/OMA_AUDIT_DATA")
display(wrangler_sample_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

oma_path = "abfss://eb87c50a-8bc7-40f8-bb1a-8a135398c6f4@onelake.dfs.fabric.microsoft.com/5677ae72-a852-4cf5-bebf-d7174c1589c0/Tables/OMA_AUDIT_DATA"
oma = spark.read.format("delta").load(oma_path)
# oma.write.format("Parquet").save("abfss://eb87c50a-8bc7-40f8-bb1a-8a135398c6f4@onelake.dfs.fabric.microsoft.com/a82c5ac8-8053-43dd-9731-33e4b08cce04/Files/OMA_AUDIT_DATA")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

oma_wrangler_df = oma.toPandas()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

oma.count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

oma_wrangler_df.count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
