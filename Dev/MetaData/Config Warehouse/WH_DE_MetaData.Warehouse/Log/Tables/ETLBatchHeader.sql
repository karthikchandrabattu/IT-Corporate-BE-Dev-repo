CREATE TABLE [Log].[ETLBatchHeader] (

	[BatchId] int NULL, 
	[PipelineName] varchar(255) NULL, 
	[PipelineRunId] varchar(255) NULL, 
	[StartTime] datetime2(6) NULL, 
	[EndTime] datetime2(6) NULL, 
	[DurationInMinutes] bigint NULL, 
	[Status] varchar(255) NULL, 
	[ErrorMessage] varchar(600) NULL
);