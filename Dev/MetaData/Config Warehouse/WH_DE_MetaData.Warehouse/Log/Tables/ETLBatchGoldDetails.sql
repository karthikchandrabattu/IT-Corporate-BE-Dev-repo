CREATE TABLE [Log].[ETLBatchGoldDetails] (

	[BatchId] varchar(max) NULL, 
	[TableId] varchar(max) NULL, 
	[SchemaName] varchar(max) NULL, 
	[TableName] varchar(max) NULL, 
	[StartTime] varchar(max) NULL, 
	[EndTime] varchar(max) NULL, 
	[DurationInSec] varchar(max) NULL, 
	[BronzeDataRead] varchar(max) NULL, 
	[DataTypeCasting] varchar(max) NULL, 
	[SilverCount] varchar(max) NULL, 
	[GoldCount] varchar(max) NULL, 
	[GoldDataLoad] varchar(max) NULL, 
	[ErrorMessage] varchar(max) NULL, 
	[Status] varchar(max) NULL, 
	[EtlLoadedBy] varchar(max) NULL, 
	[ItemType] varchar(255) NULL
);