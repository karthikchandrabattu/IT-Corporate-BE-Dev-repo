CREATE   PROCEDURE [Log].[usp_UpdateETLLogDetails]
    @BatchId  VARCHAR(255) ,  
	@LoadType VARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY

        INSERT INTO [Log].[ETLLogDetails] (
            BatchId, TableId, SchemaName, TableName,
            PipelineId, PipelineRunId, DataReadSize, DataWrittenSize,
            ThroughputValue, FilesProcessedCount, SourceName,
            BronzeStartTime, BronzeEndTime, BronzeDuration,
            BronzeCount, BronzeStatus, BronzeErrorMessage,
            SilverStartTime, SilverEndTime, SilverDurationInSec,
            SilverDataTypeCasting, SilverCount, SilverStatus, SilverErrorMessage,
            GoldStartTime, GoldEndTime, GoldDurationInSec,
            GoldDataTypeCasting, GoldCount, GoldErrorMessage, GoldStatus,
            EtlLoadedBy, LoadType, ItemType)
        SELECT
            b.BatchId,
            b.TableId,
            b.SchemaName,
            b.TableName,
            b.PipelineId,
            b.PipelineRunId,
            b.DataReadSize,
            b.DataWrittenSize,
            b.ThroughputValue,
            b.FilesProcessedCount,
            b.SourceName,
            /* ------------  Bronze ------------ */
            b.StartTime      AS BronzeStartTime,
            b.EndTime        AS BronzeEndTime,
            b.Duration       AS BronzeDuration,
            b.[RowCount]       AS BronzeCount,
            b.Status         AS BronzeStatus,
            b.ErrorMessage   AS BronzeErrorMessage,
            /* ------------  Silver ------------ */
            s.StartTime      AS SilverStartTime,
            s.EndTime        AS SilverEndTime,
            s.DurationInSec  AS SilverDurationInSec,
            s.DataTypeCasting,
            s.SilverCount,
            s.Status         AS SilverStatus,
            s.ErrorMessage   AS SilverErrorMessage,
            /* ------------   Gold  ------------ */
            g.StartTime      AS GoldStartTime,
            g.EndTime        AS GoldEndTime,
            g.DurationInSec  AS GoldDurationInSec,
            g.DataTypeCasting,
            g.GoldCount,
            g.ErrorMessage   AS GoldErrorMessage,
            g.Status         AS GoldStatus,
            g.EtlLoadedBy,
			@LoadType,
            CONCAT('Bronze Load - ',b.ItemType, ', Silver Load - ',s.ItemType, ', Gold Load - ',g.ItemType)
        FROM  [Log].[ETLBatchBronzeDetails]  AS b  
        LEFT JOIN [Log].[ETLBatchSilverDetails]  AS s  
               ON  s.BatchId = b.BatchId  AND s.TableId = b.TableId
        LEFT JOIN [Log].[ETLBatchGoldDetails]    AS g  
               ON  g.BatchId = b.BatchId  AND g.TableId = b.TableId
        WHERE b.BatchId = @BatchId;

    END TRY
    BEGIN CATCH

        DECLARE
            @ErrMsg  NVARCHAR(2048) = ERROR_MESSAGE(),
            @ErrNum  INT            = ERROR_NUMBER(),
            @ErrProc SYSNAME        = ERROR_PROCEDURE()

        /* Optional persistent logging – create table beforehand if wanted */
        --INSERT INTO [Log].[ETL_StoredProcErrors]
        --        (ProcName, ErrorNumber, ErrorMessage, ErrorLine, BatchId, ErrorDate)
        --VALUES (@ErrProc, @ErrNum, @ErrMsg, @ErrLine, @BatchId, SYSDATETIME());

        RAISERROR (
            'usp_UpdateETLLogDetails failed (%d – %s). See error log for detail.',
            16, 1, @ErrNum, @ErrMsg);
    END CATCH
END