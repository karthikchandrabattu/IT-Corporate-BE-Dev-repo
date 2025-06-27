CREATE    PROCEDURE [dbo].[StartSFTPFileDownloadLog_Updated]
    @FilePath VARCHAR(500),
	@BatchID BIGINT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @LogID BIGINT;

	SELECT @LogID = ABS(CHECKSUM(NEWID()));

    -- Insert only one record per file
    INSERT INTO dbo.SFTPFileDownloadLog (LogID, BatchID, FileName, FilePath, DownloadTimestamp, Status, ErrorMessage, RowsCopied)
    VALUES (@LogID, @BatchID, NULL, @FilePath, GETUTCDATE() AT TIME ZONE 'UTC' AT TIME ZONE 'Eastern Standard Time', 'InProgress', NULL, NULL);

    PRINT 'SFTP file download started. LogID: ' + CAST(@LogID AS VARCHAR);
    SELECT @LogID AS LogID;
END;