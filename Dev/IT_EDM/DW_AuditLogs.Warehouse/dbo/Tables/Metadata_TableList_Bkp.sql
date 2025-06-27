CREATE TABLE [dbo].[Metadata_TableList_Bkp] (

	[ID] int NOT NULL, 
	[SourceSystemName] varchar(50) NOT NULL, 
	[SourceDatabaseName] varchar(50) NOT NULL, 
	[SourceSchemaName] varchar(50) NULL, 
	[SourceTableName] varchar(50) NOT NULL, 
	[TargetTableName] varchar(50) NOT NULL, 
	[LoadType] varchar(50) NOT NULL, 
	[FilterColumnName] varchar(50) NULL, 
	[TargetDataLoadType] varchar(50) NULL, 
	[BronzeLoadStatus] varchar(50) NULL, 
	[BronzeLoadRunDate] datetime2(6) NULL, 
	[SilverLoadStatus] varchar(50) NULL, 
	[SilverLoadRunDate] datetime2(6) NULL, 
	[IsActive] bit NOT NULL, 
	[SourceColumnList] varchar(50) NULL, 
	[KeyColumnList] varchar(50) NULL, 
	[ETLRefresh_Timestamp] datetime2(6) NULL
);