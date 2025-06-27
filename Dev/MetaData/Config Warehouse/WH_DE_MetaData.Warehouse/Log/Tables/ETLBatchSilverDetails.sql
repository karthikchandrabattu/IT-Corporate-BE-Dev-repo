CREATE TABLE [Log].[ETLBatchSilverDetails] (

	[BatchId] varchar(max) NULL, 
	[TableId] varchar(max) NULL, 
	[SchemaName] varchar(max) NULL, 
	[TableName] varchar(max) NULL, 
	[StartTime] varchar(max) NULL, 
	[EndTime] varchar(max) NULL, 
	[DurationInSec] varchar(max) NULL, 
	[BronzeDataRead] varchar(max) NULL, 
	[DataTypeCasting] varchar(max) NULL, 
	[BronzeCount] varchar(max) NULL, 
	[SilverCount] varchar(max) NULL, 
	[SilverDataLoad] varchar(max) NULL, 
	[ErrorMessage] varchar(max) NULL, 
	[Status] varchar(max) NULL, 
	[EtlLoadedBy] varchar(max) NULL, 
	[ItemType] varchar(255) NULL
);