CREATE   PROCEDURE dbo.usp_MasterTriggerSP
AS

PRINT 'Running SP - 1...'
EXEC  dbo.usp_SelectTable1

PRINT 'Running SP - 2...'
EXEC  dbo.usp_SelectTable2

PRINT 'Running SP - 3...'
EXEC  dbo.usp_SelectTable3