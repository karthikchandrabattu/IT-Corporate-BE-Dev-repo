/*=====================================================================
    dbo.usp_GetUnmatchedTables
=====================================================================*/
CREATE PROCEDURE dbo.usp_GetUnmatchedTables
    @DBSource sysname                 -- e.g. 'EDW'
AS
BEGIN
    SET NOCOUNT ON;

    ------------------------------------------------------------------
    -- 1. Build a safely-quoted three-part object name:
    --    [DE_LH_Silver].[meta].[SourceInformationSchema_<DBSource>]
    ------------------------------------------------------------------
    DECLARE @safeTableName  sysname = QUOTENAME
        (N'SourceInformationSchema_' + REPLACE(@DBSource, N']', N']]'));

    DECLARE @fullObjectName nvarchar(MAX) = 
          QUOTENAME(N'DE_LH_Silver') + N'.'
        + QUOTENAME(N'meta')         + N'.'
        + @safeTableName;

    ------------------------------------------------------------------
    -- 2. Dynamic query
    ------------------------------------------------------------------
    DECLARE @sql nvarchar(MAX) = N'
;WITH TableList AS
(
    SELECT DISTINCT si.TABLE_NAME
    FROM ' + @fullObjectName + N' AS ssi
    RIGHT JOIN WH_DE_MetaData.Config.SQLServerSourceInformationSchema AS si
           ON  ssi.TABLE_SCHEMA = si.TABLE_SCHEMA
           AND ssi.TABLE_NAME   = si.TABLE_NAME
           AND ssi.COLUMN_NAME  = si.COLUMN_NAME
           AND ssi.DATA_TYPE    = si.DATA_TYPE
    WHERE ( ssi.TABLE_NAME  IS NULL
         OR ssi.COLUMN_NAME IS NULL
         OR ssi.DATA_TYPE   IS NULL )
      AND si.TABLE_CATALOG = @dbsource          -- ← qualified here
)
SELECT  STRING_AGG(CAST(ConfigId AS varchar(20)), '','') AS ConfigList ,
        STRING_AGG(SourceTableName,               '','') AS TableList
FROM    WH_DE_MetaData.Config.MetaETL
WHERE   SourceTableName IN (SELECT TABLE_NAME FROM TableList);';

    ------------------------------------------------------------------
    -- 3. Execute safely, passing @DBSource as a parameter
    ------------------------------------------------------------------
    EXEC sys.sp_executesql
        @sql,
        N'@dbsource sysname',
        @dbsource = @DBSource;
END;