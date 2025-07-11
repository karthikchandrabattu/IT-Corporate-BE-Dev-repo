CREATE TABLE [Log].[ETLLogDetails] (

	[BatchId] varchar(255) NOT NULL, 
	[TableId] int NOT NULL, 
	[SchemaName] varchar(255) NOT NULL, 
	[TableName] varchar(255) NOT NULL, 
	[PipelineId] varchar(255) NULL, 
	[PipelineRunId] varchar(255) NULL, 
	[DataReadSize] varchar(255) NULL, 
	[DataWrittenSize] varchar(255) NULL, 
	[ThroughputValue] varchar(255) NULL, 
	[FilesProcessedCount] bigint NULL, 
	[SourceName] varchar(255) NULL, 
	[BronzeStartTime] datetime2(6) NULL, 
	[BronzeEndTime] datetime2(6) NULL, 
	[BronzeDuration] bigint NULL, 
	[BronzeCount] bigint NULL, 
	[BronzeStatus] varchar(255) NULL, 
	[BronzeErrorMessage] varchar(8000) NULL, 
	[SilverStartTime] varchar(max) NULL, 
	[SilverEndTime] varchar(max) NULL, 
	[SilverDurationInSec] varchar(max) NULL, 
	[SilverDataTypeCasting] varchar(max) NULL, 
	[SilverCount] varchar(max) NULL, 
	[SilverStatus] varchar(max) NULL, 
	[SilverErrorMessage] varchar(max) NULL, 
	[GoldStartTime] varchar(max) NULL, 
	[GoldEndTime] varchar(max) NULL, 
	[GoldDurationInSec] varchar(max) NULL, 
	[GoldDataTypeCasting] varchar(max) NULL, 
	[GoldCount] varchar(max) NULL, 
	[GoldErrorMessage] varchar(max) NULL, 
	[GoldStatus] varchar(max) NULL, 
	[EtlLoadedBy] varchar(max) NULL, 
	[LoadType] varchar(255) NULL, 
	[ItemType] varchar(255) NULL
);