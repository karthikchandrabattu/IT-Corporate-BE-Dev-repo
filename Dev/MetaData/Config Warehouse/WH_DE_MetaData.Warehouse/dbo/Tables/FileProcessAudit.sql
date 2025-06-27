CREATE TABLE [dbo].[FileProcessAudit] (

	[BatchID] int NULL, 
	[PipelineID] varchar(1000) NULL, 
	[FolderName] varchar(1000) NULL, 
	[PipelineTriggerTime] datetime2(6) NULL, 
	[Status] varchar(1000) NULL
);