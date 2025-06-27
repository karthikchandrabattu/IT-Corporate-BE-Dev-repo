CREATE PROCEDURE [dbo].[usp_BRZProcess_OnEnd] 
	@ETLBatchID BIGINT,
	@status BIGINT,
	@BatchEnd DATETIME2(3),
	@SourceCount BIGINT,
	@StageCount BIGINT,
	@ErrorMessage VARCHAR(4000),
	@BatchName VARCHAR(100),
	@CopyingDuration VARCHAR(50),
	@DataReadSize VARCHAR(50),
	@DataWriteSize VARCHAR(50),
	@FileWrittenToADLS VARCHAR(200),
	@ThroughputValue FLOAT,
	@Description VARCHAR(100) = NULL,
	@BatchStart DATETIME2(3) = NULL
AS
BEGIN
	SET NOCOUNT ON;
	SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

	IF @Description = 'Loading Source to Bronze'
	BEGIN
		UPDATE dbo.Audit_ObjectExecutionLog
		SET EndTime = @BatchEnd,
			Status = CASE WHEN ISNULL(Status, 0) = 0 THEN @status ELSE Status END,
			BatchEnd = @BatchEnd,
			SourceCount = @SourceCount,
			StageCount = @StageCount,
			FileWrittenToLakehouse = @FileWrittenToADLS,
			CopyingDuration = @CopyingDuration,
			DataReadSize = @DataReadSize,
			DataWriteSize = @DataWriteSize,
			ThroughputValue = @ThroughputValue,
			Description = @Description,
			BatchStart = @BatchStart,
			SystemErrorMessage = @ErrorMessage
		WHERE BatchName = @BatchName
			AND ETLBatchID = @ETLBatchID
			AND Description = @Description
	END
	ELSE
	BEGIN
		UPDATE dbo.Audit_ObjectExecutionLog
		SET EndTime = @BatchEnd,
			Status = @status,
			BatchEnd = @BatchEnd,
			SourceCount = @SourceCount,
			StageCount = @StageCount,
			Description = @Description,
			BatchStart = @BatchStart,
			SystemErrorMessage = @ErrorMessage
		WHERE BatchName = @BatchName
			AND ETLBatchID = @ETLBatchID
			AND Description = @Description
	END

	SET NOCOUNT OFF
END