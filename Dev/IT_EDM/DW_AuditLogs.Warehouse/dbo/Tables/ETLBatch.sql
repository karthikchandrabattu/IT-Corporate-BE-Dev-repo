CREATE TABLE [dbo].[ETLBatch] (

	[ETLBatchID] int NOT NULL, 
	[BatchStartTime] datetime2(6) NULL, 
	[BatchEndTime] datetime2(6) NULL, 
	[BatchStatus] int NULL, 
	[SourceSystem] varchar(50) NULL, 
	[LoadState] varchar(20) NULL, 
	[TriggerType] varchar(50) NULL
);