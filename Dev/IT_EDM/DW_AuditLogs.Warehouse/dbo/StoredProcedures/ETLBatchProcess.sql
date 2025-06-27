CREATE PROCEDURE [dbo].[ETLBatchProcess]
    @IsForceStartRequired BIT,
    @SourceSystem VARCHAR(50),
    @TriggerType VARCHAR(50),
    @LoadState VARCHAR(30)
AS
BEGIN
    SET NOCOUNT ON;
	SET TRANSACTION ISOLATION LEVEL READ COMMITTED

    BEGIN TRY
        -- Declare variables to hold batch details
        DECLARE @ETLBatchID INT;
        DECLARE @BatchStartTime DATETIME;
        DECLARE @BatchEndTime DATETIME;
        DECLARE @CurrentLoadState VARCHAR(30);

        -- Declare variables to check the last batch
        DECLARE @LastBatchStatus INT;
        DECLARE @LastBatchID INT;
        DECLARE @LastBatchStartTime DATETIME;
        DECLARE @LastBatchEndTime DATETIME;
        DECLARE @LastLoadState VARCHAR(30);

        -- Fetch the last batch details for the given SourceSystem and TriggerType
        SELECT TOP 1 
            @LastBatchStatus = BatchStatus,
            @LastBatchID = ETLBatchID,
            @LastBatchStartTime = BatchStartTime,
            @LastBatchEndTime = BatchEndTime,
            @LastLoadState = LoadState
        FROM dbo.ETLBatch
        WHERE SourceSystem = @SourceSystem
          AND TriggerType = @TriggerType
        ORDER BY BatchStartTime DESC;

        -- Decide whether to create a new batch
        IF @IsForceStartRequired = 1 OR @LastBatchStatus IS NULL OR @LastBatchStatus = 2
        BEGIN
            -- Generate a new ETLBatchID by finding the maximum existing ID and adding 1
            SELECT @ETLBatchID = ISNULL(MAX(ETLBatchID), 0) + 1 FROM dbo.ETLBatch;

            -- Set BatchStartTime and CurrentLoadState
            --SET @BatchStartTime = GETDATE();

			SET @BatchStartTime = GETDATE() AT TIME ZONE 'UTC' AT TIME ZONE 'Eastern Standard Time';

            SET @CurrentLoadState = @LoadState;

            -- Insert a new batch entry
            INSERT INTO dbo.ETLBatch (
                ETLBatchID, BatchStartTime, BatchEndTime, BatchStatus, SourceSystem, LoadState, TriggerType
            )
            VALUES (
                @ETLBatchID,
                @BatchStartTime, -- Current timestamp as start time
                NULL, -- BatchEndTime is NULL initially
                0, -- BatchStatus = 0 ("In Progress")
                @SourceSystem,
                @CurrentLoadState,
                @TriggerType
            );

            -- Select the new batch details
            SELECT 
                @ETLBatchID AS ETLBatchID,
                @BatchStartTime AS BatchStartTime,
                NULL AS BatchEndTime,
                @CurrentLoadState AS CurrentLoadState;

            PRINT 'New ETL Batch created successfully.';
        END
        ELSE
        BEGIN
            -- If the last batch is incomplete or failed, return its details
            SET @ETLBatchID = @LastBatchID;
            SET @BatchStartTime = @LastBatchStartTime;
            SET @BatchEndTime = @LastBatchEndTime;
            SET @CurrentLoadState = @LastLoadState;

            -- Select the existing batch details
            SELECT 
                @ETLBatchID AS ETLBatchID,
                @BatchStartTime AS BatchStartTime,
                @BatchEndTime AS BatchEndTime,
                @CurrentLoadState AS CurrentLoadState;

            PRINT 'Previous batch is either incomplete or failed. Returning existing batch details.';
        END
    END TRY
    BEGIN CATCH
        -- Handle errors
        PRINT 'An error occurred: ' + ERROR_MESSAGE();
        THROW; -- Re-throw the error for higher-level handling
    END CATCH
END;