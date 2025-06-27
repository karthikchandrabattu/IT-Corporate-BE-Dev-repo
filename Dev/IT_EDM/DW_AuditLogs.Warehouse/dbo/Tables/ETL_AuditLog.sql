CREATE TABLE [dbo].[ETL_AuditLog] (

	[LogID] int NOT NULL, 
	[ProcessName] varchar(100) NOT NULL, 
	[StartTime] datetime2(3) NOT NULL, 
	[EndTime] datetime2(3) NULL, 
	[Status] varchar(20) NOT NULL, 
	[ErrorMessage] varchar(4000) NULL, 
	[SourceFileCount] int NULL, 
	[TargetRowCount] int NULL, 
	[CopyingDurationFormatted] varchar(20) NULL, 
	[LastUpdated] datetime2(3) NOT NULL, 
	[LatestProcessedFileName] varchar(max) NULL
);