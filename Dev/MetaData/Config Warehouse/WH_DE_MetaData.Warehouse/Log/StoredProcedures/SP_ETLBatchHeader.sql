/*============================================================
  Script 3 ‒ Stored procedure: LOG.SP_ETLBatchHeader
============================================================*/
CREATE   PROCEDURE [Log].[SP_ETLBatchHeader]
    @PipelineName      VARCHAR(255),
    @PipelineRunId     VARCHAR(255),
    @StartTime         DATETIME2(6) = NULL,
    @EndTime           DATETIME2(6) = NULL,
    @Status            VARCHAR(800)  = NULL,
    @ErrorMessage      VARCHAR(800)  = NULL,
    @BatchId           BIGINT        = NULL
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @DurationInMinutes INT = NULL;
    --Check BatchID exists or not
    IF @BatchId IS NOT NULL
    BEGIN
        IF @StartTime > @EndTime
        BEGIN
            RAISERROR('StartTime cannot be greater than EndTime.', 16, 1);
            RETURN;
        END;

        IF @StartTime IS NOT NULL AND @EndTime IS NOT NULL
            SET @DurationInMinutes = DATEDIFF(MINUTE, @StartTime, @EndTime);

        UPDATE [Log].[ETLBatchHeader]
        SET    EndTime           = @EndTime,
               Status            = @Status,
               DurationInMinutes = @DurationInMinutes,
               ErrorMessage      = @ErrorMessage
        WHERE  BatchId = @BatchId;

        RETURN;
    END;

    -- ► Otherwise insert a new record
    DECLARE @NewBatchId INT;
    SELECT @NewBatchId = ISNULL(MAX(BatchId), 0) + 1
    FROM   [Log].[ETLBatchHeader];

    IF @StartTime IS NOT NULL AND @EndTime IS NOT NULL
        SET @DurationInMinutes = DATEDIFF(MINUTE, @StartTime, @EndTime);

    INSERT INTO [Log].[ETLBatchHeader] (
        BatchId, PipelineName, PipelineRunId,
        StartTime, EndTime, DurationInMinutes,
        Status, ErrorMessage
    )
    VALUES (
        @NewBatchId, @PipelineName, @PipelineRunId,
        @StartTime, @EndTime, @DurationInMinutes,
        @Status, @ErrorMessage
    );

    SELECT @NewBatchId AS NewBatchId, @StartTime AS StartTime;  -- Return new ID if needed
END;