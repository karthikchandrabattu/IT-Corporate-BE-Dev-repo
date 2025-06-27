CREATE TABLE [dbo].[SFTPBatchAuditLog] (

	[BatchID] bigint NOT NULL, 
	[StartTime] datetime2(3) NOT NULL, 
	[EndTime] datetime2(3) NULL, 
	[TotalFiles] int NULL, 
	[SuccessCount] int NULL, 
	[FailureCount] int NULL, 
	[Status] varchar(20) NOT NULL, 
	[Remarks] varchar(255) NULL, 
	[PipelineID] varchar(255) NULL, 
	[PipelineName] varchar(255) NULL
);