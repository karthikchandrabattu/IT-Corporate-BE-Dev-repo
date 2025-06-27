CREATE TABLE [dbo].[DMD_CUST_BILLTO] (

	[BILLTO_KEY] bigint NULL, 
	[DUNS_KEY] bigint NULL, 
	[DUNSBRMERGED_KEY] bigint NULL, 
	[PRIMARY_SHIPTO_KEY] bigint NULL, 
	[BILLTO_NO] varchar(8000) NULL, 
	[BILLTO_NAME] varchar(8000) NULL, 
	[DUNS] varchar(8000) NULL, 
	[DUNS_NAME] varchar(8000) NULL, 
	[PARTNERID] varchar(8000) NULL, 
	[ACCOUNT_TYPE] varchar(8000) NULL, 
	[TERMS] varchar(8000) NULL, 
	[DTAM] decimal(17,2) NULL, 
	[OTAM] decimal(17,2) NULL, 
	[VTAM] decimal(17,2) NULL, 
	[LTAM] decimal(17,2) NULL, 
	[CREDIT_CODE] varchar(8000) NULL, 
	[CREDIT_WATCH] varchar(8000) NULL
);