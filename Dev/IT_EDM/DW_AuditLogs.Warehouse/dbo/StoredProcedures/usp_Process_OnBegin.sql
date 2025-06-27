CREATE PROCEDURE [dbo].[usp_Process_OnBegin]   
  @DWBatchId BIGINT,  
  @PipelineID VARCHAR(100) = NULL,
  @RunID VARCHAR(100) = NULL,
  @ActivityName VARCHAR(100) = NULL,
  @Description VARCHAR(100) = NULL,  
  @BatchName VARCHAR(100),  
  @ProcessDate DATETIME = NULL,  
  @StartTime DATETIME,  
  @ListType VARCHAR(20) = NULL,  
  @ListID BIGINT = NULL  
AS  
BEGIN  
  SET NOCOUNT ON;
  SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

  BEGIN TRY  
    SET @ProcessDate = ISNULL(@ProcessDate, GETDATE());

    INSERT INTO [dbo].[Audit_ObjectExecutionLog] (  
       ETLBatchID,
       PipelineID,
       RunID,
       ActivityName,
       [Description],  
       BatchName,  
       ProcessDate,  
       StartTime,  
       EndTime,  
       [Status],  
       SystemErrorMessage,  
       ListType,  
       ListID  
    )  
    VALUES (  
       @DWBatchId,
       @PipelineID,
       @RunID,
       @ActivityName,
       @Description,  
       @BatchName,  
       CAST(@ProcessDate AS DATE),  
       @StartTime,  
       NULL,  
       0,   
       NULL,        
       @ListType,  
       @ListID  
    );  

  END TRY  
  BEGIN CATCH  
    PRINT 'Error occurred in usp_Process_OnBegin';
  END CATCH  

  SET NOCOUNT OFF;
END