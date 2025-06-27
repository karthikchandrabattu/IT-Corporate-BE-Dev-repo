CREATE PROCEDURE [dbo].[usp_GetTablesToFetch]
	@SourceSystem 	NVARCHAR(500) = 'all',
	@SourceDB 		NVARCHAR(500) = 'all',
	@SourceTables 	NVARCHAR(MAX) = 'all',
	@ProcessStep 	NVARCHAR(500) = 'sourcetobronze',
	@RunType		NVARCHAR(500) = 'new',		
	@DWBatchId		NVARCHAR(20)
	
AS
BEGIN
	SET NOCOUNT ON

	DECLARE @Cmd NVARCHAR(1000)

	SET @Cmd = 'SELECT t.* 
				FROM dbo.Metadata_TableList t
				WHERE t.IsActive = 1 '

	
	


	IF LOWER(@SourceSystem) <> 'all' BEGIN
		SET @Cmd = @Cmd + ' AND LOWER(t.SourceSystemName) = LOWER(''' + @SourceSystem + ''') '
	END

	IF LOWER(@SourceDB) <> 'all' BEGIN
		SET @Cmd = @Cmd + ' AND LOWER(t.SourceDatabaseName) = LOWER(''' + @SourceDB + ''') '
	END

	IF LOWER(@SourceTables) <> 'all' BEGIN
		SET @Cmd = @Cmd + ' AND t.id IN (' + @SourceTables + ') '
	END

	--select @Cmd
	EXEC sp_executesql @Cmd

	SET NOCOUNT OFF
END