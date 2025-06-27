CREATE   PROCEDURE usp_UpdateflagEDMtables_based_on_status
AS
BEGIN

	UPDATE [Config].[MetaETL] SET IsActive = 0;

	UPDATE [Config].[MetaETL] SET IsActive = 1 WHERE 
	CONCAT(SourceSchemaName,'.',SourceTableName) IN (SELECT [DataSource] FROM DE_LH_Silver.meta.StatusTable WHERE Live_Status = 'Ready');

END