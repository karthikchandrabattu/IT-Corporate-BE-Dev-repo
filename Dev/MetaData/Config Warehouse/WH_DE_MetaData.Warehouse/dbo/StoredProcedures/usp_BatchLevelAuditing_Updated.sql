CREATE   PROCEDURE [dbo].[usp_BatchLevelAuditing_Updated]
    @TotalFiles INT,   -- Total files (only needed for updates)
    @Status VARCHAR(20),      -- 'InProgress', 'Completed', 'Failed'
    @Remarks VARCHAR(255) = NULL,
	@BatchID BIGINT  = NULL,
	@PipelineID VARCHAR(255),
	@PipelineName VARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

   -- DECLARE @BatchID BIGINT;

	DECLARE @NewBatchID BIGINT;
	DECLARE @FailCount INT;
	DECLARE @SucessCount INT;

    -- Validate Status
    IF @Status NOT IN ('InProgress', 'Completed', 'Failed')
    BEGIN
        PRINT 'Invalid Status. Allowed values: InProgress, Completed, Failed';
        RETURN;
    END;

    -- If starting a new batch, insert a record and return the new BatchID
    IF @Status = 'InProgress'
    BEGIN
        -- Generate a unique BatchID
        SELECT @BatchID = (SELECT COALESCE(MAX(BatchID), 0) FROM dbo.SFTPBatchAuditLog)

		SET @NewBatchID = @BatchID + 1


        -- Insert new batch record
        INSERT INTO dbo.SFTPBatchAuditLog (BatchID, StartTime, TotalFiles, Status, Remarks, PipelineID, PipelineName)
        VALUES (@NewBatchID, GETUTCDATE() AT TIME ZONE 'UTC' AT TIME ZONE 'Eastern Standard Time', 0, 'InProgress', @Remarks,@PipelineID, @PipelineName);

        PRINT 'New SFTP batch started. BatchID: ' + CAST(@NewBatchID AS VARCHAR);
        
        -- Return the new BatchID
        SELECT @NewBatchID AS BatchID;
    END
    ELSE
    BEGIN
		

        -- Updating batch record when processing ends
        UPDATE dbo.SFTPBatchAuditLog
        SET 
            EndTime = GETUTCDATE() AT TIME ZONE 'UTC' AT TIME ZONE 'Eastern Standard Time',
            TotalFiles = CAST(SuccessCount AS INT) + CAST(FailureCount AS int),
            Status = @Status,
            Remarks = @Remarks,
            SuccessCount = (SELECT COUNT(*) FROM dbo.SFTPFileDownloadLog WHERE BatchID = @BatchID AND Status = 'Success'),
            FailureCount = (SELECT COUNT(*) FROM dbo.SFTPFileDownloadLog WHERE BatchID = @BatchID AND Status = 'Failed')
        WHERE BatchID = (SELECT MAX(BatchID) FROM dbo.SFTPBatchAuditLog WHERE Status = 'InProgress');

		UPDATE dbo.SFTPBatchAuditLog
		SET TotalFiles = CAST(SuccessCount AS INT) + CAST(FailureCount AS int)
		WHERE BatchID = @BatchID

        PRINT 'SFTP batch processing updated.';
    END;
END;