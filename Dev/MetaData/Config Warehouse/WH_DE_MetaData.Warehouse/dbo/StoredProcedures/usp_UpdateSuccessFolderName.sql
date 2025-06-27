CREATE PROCEDURE [dbo].[usp_UpdateSuccessFolderName]
@FolderName VARCHAR(255),
@BatchID BIGINT,
@PipelineID VARCHAR(255),
@PipelineTriggerTime DATETIME2(6),
@Status VARCHAR(255)
AS
DECLARE @EstTime DATETIME2(6)

SET @EstTime = @PipelineTriggerTime AT TIME ZONE 'UTC' AT TIME ZONE 'Eastern Standard Time'

INSERT INTO  [dbo].[FileProcessAudit] ([BatchID],[PipelineID],[FolderName],[PipelineTriggerTime],[Status]) VALUES
(@BatchID, @PipelineID, @FolderName, @EstTime, @Status)