CREATE PROCEDURE [dbo].[usp_ETLBatchOnEnd] @ETLBatchID INT
	,@Status INT
	--,@AdlsLoad BIT
	--,@StageLoad BIT
	--,@DWLoad BIT
	,@LoadState VARCHAR(100)
	,@SystemName VARCHAR(200)
	
AS
BEGIN
	SET NOCOUNT ON;
	SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

	
	-- Updating for all successful completion (after reports completion)  
	IF @LoadState = 'complete'
		AND @Status = 1
	BEGIN
		UPDATE ETLBatch
		SET	LoadState = @LoadState
			,BatchStatus = @Status
			,BatchEndTime =  GETDATE() AT TIME ZONE 'UTC' AT TIME ZONE 'Eastern Standard Time'

		
		WHERE ETLBatchID = @ETLBatchID;
	END
			-- Updating the DW table after successfull ADLS load  
	ELSE IF @LoadState = 'SourcetoBronze'
		AND @Status = 1
	BEGIN
		UPDATE ETLBatch
		SET
			LoadState = @LoadState
		WHERE ETLBatchID = @ETLBatchID;;
	END
			-- Updating the DW table after succesfull Stage load  
	ELSE IF @LoadState = 'BronzetoSilver'
		AND @Status = 1
	BEGIN
		UPDATE ETLBatch
		SET 
			LoadState = @LoadState
			--,BatchEndTime =  GETDATE() AT TIME ZONE 'UTC' AT TIME ZONE 'Eastern Standard Time'
			--,BatchStatus = @Status
		WHERE ETLBatchID = @ETLBatchID;
	END
			-- Updating the DW table after succesfull DW load  
	ELSE IF @LoadState = 'SilvertoGold'
		AND @Status = 1
	BEGIN
		UPDATE ETLBatch
		SET
			LoadState = @LoadState
			,BatchEndTime =  GETDATE() AT TIME ZONE 'UTC' AT TIME ZONE 'Eastern Standard Time'
			,BatchStatus = @Status

		WHERE ETLBatchID = @ETLBatchID;
	END

	SET NOCOUNT OFF
END