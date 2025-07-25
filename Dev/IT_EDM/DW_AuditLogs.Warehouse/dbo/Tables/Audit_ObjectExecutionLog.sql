CREATE TABLE [dbo].[Audit_ObjectExecutionLog] (

	[ETLBatchID] bigint NULL, 
	[PipelineID] varchar(100) NULL, 
	[RunID] varchar(100) NULL, 
	[BatchName] varchar(100) NOT NULL, 
	[ActivityName] varchar(100) NULL, 
	[ProcessDate] date NOT NULL, 
	[BatchStart] datetime2(3) NULL, 
	[BatchEnd] datetime2(3) NULL, 
	[StartTime] datetime2(3) NOT NULL, 
	[EndTime] datetime2(3) NULL, 
	[Status] bigint NOT NULL, 
	[SystemErrorMessage] varchar(4000) NULL, 
	[SourceCount] bigint NULL, 
	[StageCount] bigint NULL, 
	[ListType] varchar(20) NULL, 
	[ListID] bigint NULL, 
	[FileWrittenToLakehouse] varchar(200) NULL, 
	[CopyingDuration] varchar(50) NULL, 
	[DataReadSize] varchar(50) NULL, 
	[DataWriteSize] varchar(50) NULL, 
	[ThroughputValue] float NULL, 
	[Description] varchar(100) NULL
);