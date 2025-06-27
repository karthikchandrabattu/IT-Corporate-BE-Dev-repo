/*============================================================
  Script 4 ‒ Stored procedure: LOG.SP_ETLBatchBronzeDetails
============================================================*/
CREATE   PROCEDURE [Log].[SP_ETLBatchBronzeDetails]
    @BatchId            VARCHAR(255),
    @TableName          VARCHAR(255),
    @TableId            INT,
    @SchemaName         VARCHAR(255),
    @PipelineId VARCHAR(255),
    @PipelineRunId VARCHAR(255),
    @DataReadSize VARCHAR(255),
    @DataWrittenSize VARCHAR(255),
    @ThroughputValue VARCHAR(255),
    @RowCount           BIGINT        = NULL,
    @FilesProcessedCount BIGINT       = NULL,
    @StartTime          DATETIME2(6)  = NULL,
    @EndTime            DATETIME2(6)  = NULL,
    @Duration           BIGINT = NULL,
    @Status             VARCHAR(255)  = NULL,
    @ErrorMessage       VARCHAR(MAX)  = NULL,
    @SourceName         VARCHAR(500),
    @ItemType VARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO [Log].[ETLBatchBronzeDetails] (
        BatchId, TableName, SchemaName,
        PipelineId, PipelineRunId, DataReadSize,
        DataWrittenSize, ThroughputValue,
        [RowCount], FilesProcessedCount,
        StartTime, EndTime, Duration, Status,
        ErrorMessage, SourceName, TableId, ItemType
    )
    VALUES (
        @BatchId, @TableName, @SchemaName,
        @PipelineId, @PipelineRunId, @DataReadSize,
        @DataWrittenSize, @ThroughputValue,
        @RowCount, @FilesProcessedCount,
        @StartTime, @EndTime, @Duration, @Status,
        @ErrorMessage, @SourceName, @TableId, @ItemType
    );
END;