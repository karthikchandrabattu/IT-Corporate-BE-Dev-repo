CREATE TABLE [dbo].[ETLBatchLog] (

	[ETLBatchID] int NOT NULL, 
	[BatchStartTime] datetime2(3) NOT NULL, 
	[BatchEndTime] datetime2(3) NULL, 
	[BatchStatus] int NOT NULL
);