CREATE TABLE [Log].[ETLBatchBronzeDetails] (

	[BatchId] varchar(255) NOT NULL, 
	[TableId] int NOT NULL, 
	[SchemaName] varchar(255) NOT NULL, 
	[TableName] varchar(255) NOT NULL, 
	[PipelineId] varchar(255) NULL, 
	[PipelineRunId] varchar(255) NULL, 
	[DataReadSize] varchar(255) NULL, 
	[DataWrittenSize] varchar(255) NULL, 
	[ThroughputValue] varchar(255) NULL, 
	[RowCount] bigint NULL, 
	[FilesProcessedCount] bigint NULL, 
	[StartTime] datetime2(6) NULL, 
	[EndTime] datetime2(6) NULL, 
	[Duration] bigint NULL, 
	[Status] varchar(255) NULL, 
	[ErrorMessage] varchar(8000) NULL, 
	[SourceName] varchar(255) NULL, 
	[ItemType] varchar(255) NULL
);