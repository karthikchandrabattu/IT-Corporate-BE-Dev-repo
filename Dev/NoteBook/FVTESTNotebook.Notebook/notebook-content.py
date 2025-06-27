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

# MARKDOWN ********************

# Generating identity column on Dataframe
# Offset is the starting point

# CELL ********************

from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("CustomerID", StringType(), True),
    StructField("Name", StringType(), True),
    StructField("Age", IntegerType(), True)
])

data = [("c4e52c13-0e57-40a2-91c6-f77b05df2b7b", "John Doe", 30),
        ("6810c6b7-8eef-4548-9ebe-8a49a56a8f3c", "Jane Smith", 25),
        ("9c9731ee-dc8e-41b7-9b82-5a07125a9711", "Alice Johnson", 35),
        ("fc6a12e4-cd42-4ba9-83bc-8b2eb5b9de39", "Bob Brown", 40),
        ("df78f45d-72e3-4ae8-b9a2-7015c8883be2", "Emily Davis", 28),
        ("1b9246a9-53e3-4df8-aeb4-7d8f6c82c90d", "Michael Wilson", 45),
        ("2f1f88b3-fc8d-47b1-9a76-cf0ccf30e212", "Samantha Taylor", 32),
        ("b660f4a9-6f2b-4f02-a95c-4818ff2e04b8", "David Martinez", 27),
        ("d86b66a3-6317-48fb-a0c8-5c4e32802207", "Olivia Miller", 38),
        ("3df597eb-b7f1-4e85-8f24-674a58d1a3cc", "William Garcia", 33)]

df = spark.createDataFrame(data, schema)

offset = 2

rdd_with_index = df.rdd.zipWithIndex()
rdd_with_index = rdd_with_index.map(lambda row: row[0] + (row[1] + offset,))
result_df = rdd_with_index.toDF(df.columns + ['IdentityId'])

display(result_df)

#df.rdd.getNumPartitions()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


import pandas as pd

# Read the document (assuming it's a CSV file)
df = pd.read_csv("/lakehouse/default/Files/TranslationTest.csv")

# Translate the text column to Spanish
df["translated_text"] = df["text_column"].ai.translate("french")

# Save the translated document
df.to_csv("Files/translated_document.csv", index=False)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
