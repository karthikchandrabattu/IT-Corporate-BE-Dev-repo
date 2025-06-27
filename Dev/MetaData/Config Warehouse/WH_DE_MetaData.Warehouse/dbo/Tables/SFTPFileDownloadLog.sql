CREATE TABLE [dbo].[SFTPFileDownloadLog] (

	[LogID] bigint NOT NULL, 
	[BatchID] bigint NOT NULL, 
	[FileName] varchar(255) NULL, 
	[FilePath] varchar(500) NOT NULL, 
	[DownloadTimestamp] datetime2(3) NOT NULL, 
	[Status] varchar(20) NOT NULL, 
	[ErrorMessage] varchar(100) NULL, 
	[RowsCopied] bigint NULL
);