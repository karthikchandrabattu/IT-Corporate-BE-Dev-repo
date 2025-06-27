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

# CELL ********************

############################################# IMPORTING REQUIRED PACKAGES ##############################################
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import (
col, lit, concat, when, trim, collect_list, row_number, to_date,date_format,
col, concat, lit, to_timestamp, date_format, to_date, coalesce,concat_ws, md5,
udf , concat, to_timestamp,count, when ,  sum as _sum)
from pyspark.sql.window import Window
from datetime import datetime, timezone, timedelta
from delta.tables import DeltaTable
import pandas as pd
from com.microsoft.spark.fabric import Constants
import com.microsoft.spark.fabric
from com.microsoft.spark.fabric.Constants import Constants
from pyspark.sql.types import (
    DoubleType, IntegerType, BooleanType, StringType,StructField,ArrayType,
    BinaryType, TimestampType, DateType, LongType, StructType
)
import concurrent.futures
import pytz
import traceback
import os
import json

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# PARAMETERS CELL ********************

################################################### NOTEBOOK PARAMETERS ####################################################
BatchId = 49

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

################################################### NOTEBOOK VARIABLES ####################################################
current_utc_time = datetime.now(timezone.utc)
user_name = mssparkutils.env.getUserName()
ETLBatchId = BatchId
BASE_ABFSS_PATH = "abfss://eb87c50a-8bc7-40f8-bb1a-8a135398c6f4@onelake.dfs.fabric.microsoft.com/89412544-9ac3-4f39-a42d-09c035b68d13/Tables"
SILVER_ABFSS_PATH = "abfss://eb87c50a-8bc7-40f8-bb1a-8a135398c6f4@onelake.dfs.fabric.microsoft.com/16fadab9-4226-43b4-885a-6f54f0951826/Tables"


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

################################################### BUILDING CUSTOM SPARK SESSION ####################################################
spark = SparkSession.builder \
    .appName("OracleDataLoad") \
    .config("spark.sql.parquet.int96RebaseModeInRead", "CORRECTED") \
    .config("spark.sql.parquet.int96RebaseModeInWrite", "CORRECTED") \
    .config("spark.sql.parquet.datetimeRebaseModeInWrite", "CORRECTED") \
    .config("spark.sql.parquet.datetimeRebaseModeInRead", "CORRECTED") \
    .config("spark.gluten.enabled", "false") \
    .config("spark.sql.legacy.parquet.datetimeRebaseModeInWrite", "CORRECTED") \
    .config("spark.sql.legacy.parquet.datetimeRebaseModeInRead", "CORRECTED") \
    .config("spark.sql.caseSensitive", "true") \
    .config("spark.sql.extensions", "delta.sql.DeltaSparkSessionExtensions") \
    .config("spark.sql.catalog.spark_catalog", "delta.catalog.DeltaCatalog") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY")\
    .getOrCreate()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

################################################### LOADING METADATA ####################################################
try:
    ConfigQuery = "SELECT * FROM Config.MetaETL"
    InformationSchema="SELECT * FROM Config.SQLServerSourceInformationSchema"
    ConfigETL_df= spark.read.option(Constants.DatabaseName, "WH_DE_MetaData").synapsesql(ConfigQuery) 
    InformationSchema_df= spark.read.option(Constants.DatabaseName, "WH_DE_MetaData").synapsesql(InformationSchema) 
except Exception as e:
    print(e)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

################################################### GETTING LIST OF BRONZE SUCCESS TABLES ####################################################
try:
    BronzeLogDetails = f"SELECT * FROM Log.ETLBatchBronzeDetails WHERE BatchId = {ETLBatchId}"
    print(BronzeLogDetails)
    success_df = spark.read \
      .option(Constants.DatabaseName, "WH_DE_MetaData") \
        .synapsesql(BronzeLogDetails)
    success_df = success_df.filter(col("Status") == 'Success') \
                          .select(col("TableId"))
    table_ids = [row.TableId for row in success_df.collect()]
    ConfigETL_df = ConfigETL_df.filter(col("ConfigId").isin(table_ids))
except Exception as e:
    print(f"Error occurred: {str(e)}")
    raise

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": true
# META }

# CELL ********************

################################################### USER DEFINED FUNCTION 1.EXTRACT BRONZE DATA ####################################################
def Read_bronze_data(bronze_schema_name: str, bronze_table_name: str) -> tuple[int, DataFrame, str, str]:
    is_okay = 1
    error_message = None
    message = ''
    bronze_df = None

    try:
        read_type = 'delta'
        relative_path = f"{bronze_schema_name}/{bronze_table_name}"
        bronze_abfss_path = f"{BASE_ABFSS_PATH}/{relative_path}"
        bronze_df = spark.read.format(read_type).load(bronze_abfss_path)
        message = f"Data successfully extracted (delta format) for Schema: {bronze_schema_name}, Table: {bronze_table_name}"            
    except Exception as e2:
        is_okay = 0
        message = f"Error extracting data for Schema: {bronze_schema_name}, Table: {bronze_table_name}"
        error_message = f"Parquet error: {str(e2)}. Delta error: {str(e2)}"
        bronze_df = None
    if bronze_df is not None:
        bronze_df = bronze_df.dropDuplicates()

    return is_okay, bronze_df, message, error_message


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

################################################### USER DEFINED FUNCTION 2.DATA TYPE CASTING ####################################################
def data_type_casting(table_name, bronze_df, config_mapping_schema_df):
    is_okay = 1
    error_message = None
    msg = 'Data Type Casting was Successful'  

    data_type_mapping = {
        "char":StringType(),
        "nchar":StringType(),
        "varchar": StringType(),
        "nvarchar": StringType(),
        "smallint": IntegerType(),
        "bit": BooleanType(),
        "int": IntegerType(),
        "bigint": LongType(),
        "date": DateType(),
        "decimal": DoubleType(),
        "datetime": TimestampType(),
        "datetime2": TimestampType(),
        "tinyint": IntegerType(),
        "uniqueidentifier": StringType(),
        "numeric":DoubleType(),
        "double": DoubleType(),
        "image": StringType(),
        "varbinary":StringType()
    }

    try:
        distinct_tables = [row['TABLE_NAME'] for row in config_mapping_schema_df.select("TABLE_NAME").distinct().toLocalIterator()]

        if table_name in distinct_tables:
            table_config = config_mapping_schema_df.filter(col("TABLE_NAME") == table_name)

            table_config_sorted = table_config.orderBy("ORDINAL_POSITION")

            for row in table_config_sorted.collect():
                column_name = row['COLUMN_NAME']
                data_type = row['DATA_TYPE']
                
                if column_name in bronze_df.columns:
                    spark_data_type = data_type_mapping.get(data_type, StringType())
                    bronze_df = bronze_df.withColumn(column_name, col(column_name).cast(spark_data_type))
                    msg = 'Data Type Casting was Completed'
                else:
                    print(f"Column '{column_name}' does not exist in the DataFrame. Skipping...")

            column_order = [row['COLUMN_NAME'] for row in table_config_sorted.collect() if row['COLUMN_NAME'] in bronze_df.columns]
            bronze_df = bronze_df.select(*column_order)

        else:
            msg = 'Data Type Casting was Not Done'

    except TypeError as e:
        is_okay = 0
        error_message = str(e)
        msg = 'Data Type Casting Failed due to Type Error'
    except ValueError as e:
        is_okay = 0
        error_message = str(e)
        msg = 'Data Type Casting Failed due to Value Error'
    except Exception as e:
        is_okay = 0
        error_message = str(e)
        msg = 'Data Type Casting Failed due to General Error'

    return is_okay, bronze_df, msg, error_message

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

####################################### USER DEFINED FUNCTION 3.ADDING WAREHOUSE AUDIT COLUMNS ##############################################
def adding_ETLWarehousing_Columns(bronze_df:DataFrame):
        is_okay = 1
        error_message = None
        msg = 'Adding ETL Warehousing Audit columns '
        current_utc_time = datetime.now(pytz.UTC)
        
        user_name = mssparkutils.env.getUserName()
        canada_time = current_utc_time + timedelta(hours=4)

        user_name = mssparkutils.env.getUserName()
        try:
            bronze_df = bronze_df.withColumn(
                                        "HashKey",
                                        md5(concat_ws("", *[col(c).cast("string") for c in bronze_df.columns]))
                                    )
            bronze_df = bronze_df.withColumn("ETLLoadedDate", lit(canada_time)) \
                                .withColumn("ETLLoadedBy", lit(user_name)) \
                                .withColumn("ETLModifiedDate", lit(canada_time)) \
                                .withColumn("ETLModifiedBy", lit(user_name)) 
            return is_okay, bronze_df, msg, error_message 
        except Exception as e:
            is_okay = 0
            error_message = str(e)
            msg= "Failed During adding warehouse Audit Columns"
            return is_okay, bronze_df, msg, error_message  

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

############################################# USER DEFINED FUNCTION 4. PERFORM INCREMENTAL LOAD FOR SILVER LAYER  ########################################################################
def silver_data_incremental_Load(spark: SparkSession, bronze_df: DataFrame, SilverTableName: str, SilverSchemaName: str, FullLoad,PrimaryKey):
    is_okay = 1
    silver_data_msg = ''
    error_message = None
    generic_path = "abfss://eb87c50a-8bc7-40f8-bb1a-8a135398c6f4@onelake.dfs.fabric.microsoft.com/16fadab9-4226-43b4-885a-6f54f0951826/Tables"
    relative_path = f"{SilverSchemaName}/{SilverTableName}"
    absolute_path = f"{generic_path}/{relative_path}"

    overwrite = 0
    pk_list = []
    dataframe = bronze_df

    try:
        try:
            if PrimaryKey:
                if isinstance(PrimaryKey, str):
                    pk_list = [col.strip() for col in PrimaryKey.split(",")]
                elif isinstance(PrimaryKey, list) and len(PrimaryKey) == 1 and isinstance(PrimaryKey[0], str) and "," in PrimaryKey[0]:
                    pk_list = [col.strip() for col in PrimaryKey[0].split(",")]
                elif isinstance(PrimaryKey, list):
                    pk_list = PrimaryKey
                else:
                    pk_list = PrimaryKey.tolist()
            else:
                overwrite = 1
        except Exception as e:
            is_okay = 0
            silver_data_msg = 'Error While Extracting PrimaryKey'
            error_message = str(e)
            return is_okay, silver_data_msg, error_message 

        if not DeltaTable.isDeltaTable(spark, absolute_path):
            try:
                dataframe.write.mode("overwrite") \
                    .format("delta") \
                    .option("overwriteSchema", "true") \
                    .save(absolute_path)
                
                silver_data_msg = 'Initial Load was completed'
                return is_okay, silver_data_msg, error_message

            except Exception as e:
                is_okay = 0
                silver_data_msg = 'Error While Performing Initial Write'
                error_message = str(e)
                return is_okay, silver_data_msg, error_message

        elif overwrite == 1 or FullLoad == 1 :
            try:
                dataframe.write.mode("overwrite") \
                    .format("delta") \
                    .option("overwriteSchema", "true") \
                    .save(absolute_path)
                if overwrite ==1:
                    silver_data_msg = 'No Primary Key performing Full Load'
                else:
                    silver_data_msg = 'performing Full Load'
                return is_okay, silver_data_msg, error_message
            except Exception as e:
                is_okay = 0
                silver_data_msg = 'Error While Performing Full Load'
                error_message = str(e)
                return is_okay, silver_data_msg, error_message

        else:
            try:
                try:
                    delta_table = DeltaTable.forPath(spark, absolute_path)
                    target_df = delta_table.toDF().select("HashKey", *pk_list)
                    source_df = dataframe.select("HashKey", *pk_list)
                except Exception as e:
                    is_okay = 0
                    silver_data_msg = 'Error While Loading the target tables'
                    error_message = str(e)
                    return is_okay, silver_data_msg, error_message
                
                try:
                    
                    filtered_source_df = dataframe.join(
                        target_df,
                        on=["HashKey"] + pk_list,
                        how="left_anti"
                    )
                except Exception as e:
                    is_okay = 0
                    silver_data_msg = 'Error While Getting new/updated records'
                    error_message = str(e)
                    return is_okay, silver_data_msg, error_message
                
                try:
                    merge_condition = " AND ".join([f"t.{k} = s.{k}" for k in pk_list])
                    merge_condition = f"({merge_condition}) AND t.HashKey != s.HashKey"

                                
                    delta_table.alias("t") \
                        .merge(
                            source_df.alias("s"),
                            merge_condition
                        ) \
                        .whenMatchedDelete() \
                        .execute()
                except Exception as e:
                    is_okay = 0
                    silver_data_msg = 'Error While Deleting old versions'
                    error_message = str(e)
                    return is_okay, silver_data_msg, error_message

                try:
                    filtered_source_df.write.mode("append") \
                        .format("delta") \
                        .option("mergeSchema", "true") \
                        .save(absolute_path)
                    new_count=filtered_source_df.count()
                    silver_data_msg = 'Merge and append operations completed ' + f'New Inserts: {new_count}'
                    return is_okay, silver_data_msg, error_message

                except Exception as e:
                    is_okay = 0
                    silver_data_msg = 'Error While Loading new/updated records'
                    error_message = str(e)
                    return is_okay, silver_data_msg, error_message

            except Exception as e:
                is_okay = 0
                silver_data_msg = 'Error in merge operation'
                error_message = str(e)
                return is_okay, silver_data_msg, error_message

    except Exception as e:
        is_okay = 0
        silver_data_msg = 'Unexpected error in incremental load'
        error_message = str(e)
        return is_okay, silver_data_msg, error_message

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

####################################### USER DEFINED FUNCTION 5.CAPTURE TABLE LEVEL LOGS  ##############################################
def update_table_level_log(log_dict,  EndTime=None, DurationInSec=None,
                            BronzeDataRead=None, DataTypeCasting=None, 
                            BronzeCount=None, SilverCount=None,
                            SilverDataLoad=None, 
                            ErrorMessage=None, Status=None):

    if EndTime is not None:
        log_dict["EndTime"] = EndTime
    if DurationInSec is not None:
        log_dict["DurationInSec"] = DurationInSec
    if BronzeDataRead is not None:
        log_dict["BronzeDataRead"] = BronzeDataRead
    if DataTypeCasting is not None:
        log_dict["DataTypeCasting"] = DataTypeCasting
    if BronzeCount is not None:
        log_dict["BronzeCount"] = BronzeCount
    if SilverCount is not None:
        log_dict["SilverCount"] = SilverCount
    if SilverDataLoad is not None:
        log_dict["SilverDataLoad"] = SilverDataLoad
    if ErrorMessage is not None:
        log_dict["ErrorMessage"] = ErrorMessage
    if Status is not None:
        log_dict["Status"] = Status
    return log_dict

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def process_table(row, InformationSchema_df,ETLBatchId):
    ################################### DECLARING THE REQUIRED VARIABLES #####################################
    start_utc_time = datetime.now(timezone.utc)
    user_name = mssparkutils.env.getUserName()
    failure_message='Not executed due to prior Failure'
    skip_message ="No new records were found; skip further processing"
    msg = None 
    bronze_count, silver_count, source_delete_count, updated_row_count, inserted_row_count = None, None, None, None, None
    
    #################################### ACCESSING THE METADATA OF THE TABLE #################################
    
    TableId = row['ConfigId']
    SourceTableName = row['SourceTableName']
    SourceSchemaName = row['SourceSchemaName']
    BronzeSchemaName = row['BronzeSchemaName']
    BronzeTableName = row['BronzeTableName']
    SilverSchemaName = row["SilverSchemaName"]
    SilverTableName = row['SilverTableName']
    FullLoad = row['IsFullLoad']
    PrimaryKey = row['PrimaryKey']

    ####################################### DICTIONARY FOR TABLE LEVEL LOG DETAILS ####################################
    TableLevelLog = {
                    "LogHeaderId": ETLBatchId,
                    "TableId":TableId,
                    "SchemaName": row['SourceSchemaName'],
                    "TableName": row['SourceTableName'],
                    "StartTime": start_utc_time,
                    "EndTime": '', 
                    "DurationInSec": '',
                    "BronzeDataRead": '',
                    "DataTypeCasting": '',
                    "BronzeCount":bronze_count,
                    "SilverCount":silver_count,
                    "SilverDataLoad": '',
                    "ErrorMessage": '',
                    "Status": '',
                    "ETLLoadedBy": user_name,
                    "ItemType": "Notebook"

    }

    print(f"Started Bronze To Silver Process for SchemaName: {BronzeSchemaName} - TableName: {SourceTableName}")
    ####################################### 1. BRONZE DATA READ ##############################################
    is_okay, bronze_df, msg, error_message = Read_bronze_data( BronzeSchemaName,SourceTableName)
    if bronze_df is None or is_okay ==0:
        TableLevelLog = update_table_level_log(
                            TableLevelLog,
                            EndTime=datetime.now(timezone.utc),
                            DurationInSec=(datetime.now(timezone.utc) - start_utc_time).total_seconds(),
                            BronzeDataRead=msg,
                            DataTypeCasting=failure_message,
                            SilverDataLoad=failure_message,
                            ErrorMessage=error_message,
                            Status="Failure"
                        )
        print(f"Error Occured while extracting the data from the bronze layer for SchemaName: {BronzeSchemaName} - TableName: {SourceTableName}")
        return TableLevelLog
    bronze_count = bronze_df.count()
    if bronze_count == 0:
        TableLevelLog = update_table_level_log(
                            TableLevelLog,
                            EndTime=datetime.now(timezone.utc),
                            DurationInSec=(datetime.now(timezone.utc) - start_utc_time).total_seconds(),
                            BronzeDataRead=msg,
                            DataTypeCasting=skip_message,
                            BronzeCount=0,
                            SilverDataLoad=skip_message,
                            ErrorMessage=None,
                            Status="Success"
                        )
        print(f"No New Record was extracting the data from the bronze layer for SchemaName: {BronzeSchemaName} - TableName: {SourceTableName}")
        return TableLevelLog

    else:
        TableLevelLog = update_table_level_log(TableLevelLog,BronzeDataRead=msg,BronzeCount= bronze_count)
    TableLevelLog = update_table_level_log(TableLevelLog)
    print("1")
    ####################################### 2. DATA TYPE CASTING ##############################################

    data_typecasting_df = InformationSchema_df.filter(((col("TABLE_NAME")==SourceTableName) & (col("TABLE_SCHEMA") == SourceSchemaName ))) 
    is_okay, bronze_df, msg, error_message = data_type_casting(SourceTableName, bronze_df, data_typecasting_df)
    if(is_okay == 0):
        TableLevelLog = update_table_level_log(
                        TableLevelLog,
                        EndTime=datetime.now(timezone.utc),
                        DurationInSec=(datetime.now(timezone.utc) - start_utc_time).total_seconds(),
                        DataTypeCasting = msg,
                        SilverDataLoad=failure_message,
                        ErrorMessage=error_message,
                        Status="Failure"
                    )
        print(f"Error Occured during data type casting for SchemaName: {BronzeSchemaName} - TableName: {SourceTableName}")
        return TableLevelLog
    else:
        TableLevelLog = update_table_level_log(TableLevelLog,DataTypeCasting=msg)   
    TableLevelLog = update_table_level_log(TableLevelLog)
    ####################################### 5. ETL WAREHOUSE AUDIT COLUMNS ##############################################

    is_okay, bronze_df, msg, error_message = adding_ETLWarehousing_Columns(bronze_df)
    if(is_okay == 0):
        TableLevelLog = update_table_level_log(
                            TableLevelLog,
                            EndTime=datetime.now(timezone.utc),
                            DurationInSec=(datetime.now(timezone.utc) - start_utc_time).total_seconds(),
                            ErrorMessage=error_message,
                            Status="Failure"
            )
         
        return TableLevelLog 
    
    ####################################### 6. SILVER LAYER DATA LOAD ##############################################
    is_okay, msg , error_message= silver_data_incremental_Load(spark,bronze_df, SilverTableName, SilverSchemaName,FullLoad, PrimaryKey)
    if(is_okay == 0):
        TableLevelLog = update_table_level_log(
                            TableLevelLog,
                            EndTime=datetime.now(timezone.utc),
                            DurationInSec=(datetime.now(timezone.utc) - start_utc_time).total_seconds(),
                            SilverDataLoad=msg,
                            ErrorMessage=error_message,
                            Status="Failure"
            )
        print(f"Data Load was Failed for SchemaName : {BronzeSchemaName} - TableName: {SourceTableName}")
        return TableLevelLog
        
    else: 
        TableLevelLog = update_table_level_log(
                            TableLevelLog,
                            EndTime=datetime.now(timezone.utc),
                            DurationInSec=(datetime.now(timezone.utc) - start_utc_time).total_seconds(),
                            SilverDataLoad=msg,
                            ErrorMessage=None,
                            Status="Success"
            )
        print(f"Data Load was Completed for SchemaName : {BronzeSchemaName} - TableName: {SourceTableName}")
    
    try:
        silver_delta_table = DeltaTable.forPath(spark, f"{SILVER_ABFSS_PATH}/{SilverSchemaName}/{SilverTableName}")
        silver_count = silver_delta_table.toDF().count()
        TableLevelLog = update_table_level_log(TableLevelLog, SilverCount=silver_count)
    except Exception as e:
        print(f"Warning: Could not get silver count for SchemaName: {BronzeSchemaName} - TableName: {SourceTableName}. Error: {str(e)}")
    
    ####################################### THE END ##############################################
    return TableLevelLog


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

################################################### EXECUTION BLOCK ####################################################
log_list = []
max_executors = 20

def process_row(row):
    return process_table(row, InformationSchema_df, ETLBatchId)

if ConfigETL_df.count() > 0:
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_executors) as executor:
            futures = {executor.submit(process_row, row): row for row in ConfigETL_df.toLocalIterator()}
            for future in concurrent.futures.as_completed(futures):
                log_entry = future.result()
                log_list.append(log_entry)
        
        if not log_list:
            print("No logs generated. Check the processing function.")
            log_df = pd.DataFrame()
        else:
            log_df = pd.DataFrame(log_list)
            log_df = log_df.astype(str)

    except Exception as e:
        print(f"An error occurred: {e}")
        log_df = pd.DataFrame(log_list)
        log_df = log_df.astype(str)

    ################################################### SAVING LOG DETAILS ####################################################
    schema = StructType([
        StructField("LogHeaderId", StringType(), True),
        StructField("TableId", StringType(), True),
        StructField("SchemaName", StringType(), True),
        StructField("TableName", StringType(), True),
        StructField("StartTime", StringType(), True),
        StructField("EndTime", StringType(), True),
        StructField("DurationInSec", StringType(), True),
        StructField("BronzeDataRead", StringType(), True),
        StructField("DataTypeCasting", StringType(), True),
        StructField("BronzeCount", StringType(), True),
        StructField("SilverCount", StringType(), True),
        StructField("SilverDataLoad", StringType(), True),
        StructField("ErrorMessage", StringType(), True),
        StructField("Status", StringType(), True),
        StructField("EtlLoadedBy", StringType(), True),
        StructField("ItemType", StringType(), True)
    ])

    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    ################################################### SAVING LOG DETAILS ####################################################
    spark_df = spark.createDataFrame(log_df, schema=schema)
    spark_df = spark_df.withColumn("BronzeCount", col("BronzeCount").cast(LongType()).cast(StringType()))
    spark_df = spark_df.withColumn("SilverCount", col("SilverCount").cast(LongType()).cast(StringType()))
    spark_df = spark_df.withColumnRenamed("LogHeaderId","BatchId")
    spark_df.write.option("overwriteSchema","true").mode("append").synapsesql("WH_DE_MetaData.Log.ETLBatchSilverDetails") 
else:
    print(f"No Tables have been executed in the Bronze Layer")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

################################################### END OF THE NOTEBOOK ####################################################

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
