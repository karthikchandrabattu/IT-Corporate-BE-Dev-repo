CREATE TABLE [dbo].[DMD_COMPANY] (

	[CMPY_KEY] bigint NULL, 
	[REGION_KEY] bigint NULL, 
	[CMPY_CODE] varchar(8000) NULL, 
	[PRIMARY_CMPY] varchar(8000) NULL, 
	[REGION] varchar(8000) NULL, 
	[REGION_ABBR] varchar(8000) NULL
);