# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "16fadab9-4226-43b4-885a-6f54f0951826",
# META       "default_lakehouse_name": "DE_LH_Silver",
# META       "default_lakehouse_workspace_id": "eb87c50a-8bc7-40f8-bb1a-8a135398c6f4",
# META       "known_lakehouses": [
# META         {
# META           "id": "16fadab9-4226-43b4-885a-6f54f0951826"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC select * into EDW_dbo.DIM_ATTMPCFL from  EDW_EDW.DIM_ATTMPCFL;
# MAGIC select * into EDW_dbo.DIM_BRANCH from  EDW_EDW.DIM_BRANCH;
# MAGIC select * into EDW_dbo.DIM_BRANCH_GROUP from  EDW_EDW.DIM_BRANCH_GROUP;
# MAGIC select * into EDW_dbo.DIM_CLASSES from  EDW_EDW.DIM_CLASSES;
# MAGIC select * into EDW_dbo.DIM_CLASS_CODE from  EDW_EDW.DIM_CLASS_CODE;
# MAGIC select * into EDW_dbo.DIM_COMPANY from  EDW_EDW.DIM_COMPANY;
# MAGIC select * into EDW_dbo.DIM_CURRENCY from  EDW_EDW.DIM_CURRENCY;
# MAGIC select * into EDW_dbo.DIM_CUSTOMER_LOCATION from  EDW_EDW.DIM_CUSTOMER_LOCATION;
# MAGIC select * into EDW_dbo.DIM_DATE from  EDW_EDW.DIM_DATE;
# MAGIC select * into EDW_dbo.DIM_GSODistribution from  EDW_EDW.DIM_GSODistribution;
# MAGIC select * into EDW_dbo.DIM_MFR from  EDW_EDW.DIM_MFR;
# MAGIC select * into EDW_dbo.DIM_MFR_FAMILY from  EDW_EDW.DIM_MFR_FAMILY;
# MAGIC select * into EDW_dbo.DIM_PM_BUSINESS_UNIT from  EDW_EDW.DIM_PM_BUSINESS_UNIT;
# MAGIC select * into EDW_dbo.DIM_RESTRICTED_CLASS from  EDW_EDW.DIM_RESTRICTED_CLASS;
# MAGIC select * into EDW_dbo.DIM_ROLE_AEG_ASSIGNMENT from  EDW_EDW.DIM_ROLE_AEG_ASSIGNMENT;
# MAGIC select * into EDW_dbo.DIM_ROLE_FGC_ASSIGNMENT from  EDW_EDW.DIM_ROLE_FGC_ASSIGNMENT;
# MAGIC select * into EDW_dbo.DIM_ROLE_GAM_ASSIGNMENT from  EDW_EDW.DIM_ROLE_GAM_ASSIGNMENT;
# MAGIC select * into EDW_dbo.DMF_VIRTUAL_INVENTORY_FOR_HYBRIS from  EDW_EDW.DMF_VIRTUAL_INVENTORY_FOR_HYBRIS;
# MAGIC select * into EDW_dbo.FACT_BACKFILL from  EDW_EDW.FACT_BACKFILL;
# MAGIC 


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
