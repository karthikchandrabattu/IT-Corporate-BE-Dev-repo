CREATE   PROCEDURE [dbo].[usp_UpdateWaterMarkValue]
@BatchId BIGINT
AS
BEGIN

UPDATE [WH_DE_MetaData].[Config].[MetaETL] SET WaterMarkValue = CAST(DATEADD(DAY, -3, GETDATE()) AS DATETIME2),
WaterMarkValue2 = CAST(DATEADD(DAY, -3, GETDATE()) AS DATETIME2)
WHERE ConfigId IN (SELECT TableId FROM WH_DE_MetaData.Log.ETLBatchGoldDetails WHERE BatchId = @BatchId)

END