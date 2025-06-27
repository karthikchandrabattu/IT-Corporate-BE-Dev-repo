CREATE   PROCEDURE dbo.usp_CreateTableFromJson
  @SchemaName SYSNAME,
  @TableName  SYSNAME,
  @JsonCols   NVARCHAR(MAX)
AS
BEGIN
  SET NOCOUNT ON;

  DECLARE 
    @FullName NVARCHAR(256) = QUOTENAME(@SchemaName) + N'.' + QUOTENAME(@TableName),
    @DDL      NVARCHAR(MAX);

  --
  -- Start building the DROP + CREATE script
  --
  SET @DDL = N'
IF OBJECT_ID(''' + @FullName + ''',''U'') IS NOT NULL
  DROP TABLE ' + @FullName + N';

CREATE TABLE ' + @FullName + N' (
';

  --
  -- Parse the JSON array and append each column definition
  --
  ;WITH Cols AS (
    SELECT
      JSON_VALUE([value], '$.COLUMN_NAME')              AS COLUMN_NAME,
      JSON_VALUE([value], '$.DATA_TYPE')                AS DATA_TYPE,
      TRY_CAST(JSON_VALUE([value], '$.CHARACTER_MAXIMUM_LENGTH') AS INT) AS CHARACTER_MAXIMUM_LENGTH,
      TRY_CAST(JSON_VALUE([value], '$.NUMERIC_PRECISION')       AS INT) AS NUMERIC_PRECISION,
      TRY_CAST(JSON_VALUE([value], '$.NUMERIC_SCALE')           AS INT) AS NUMERIC_SCALE,
      JSON_VALUE([value], '$.IS_NULLABLE')                AS IS_NULLABLE
    FROM OPENJSON(@JsonCols)
  )
  SELECT @DDL +=
    N'  ' + QUOTENAME(COLUMN_NAME) + N' ' +
    CASE
      WHEN LOWER(DATA_TYPE) IN (N'varchar', N'nvarchar')
        THEN DATA_TYPE
             + N'('
             + IIF(CHARACTER_MAXIMUM_LENGTH = -1, N'MAX', CAST(CHARACTER_MAXIMUM_LENGTH AS NVARCHAR(10)))
             + N')'
      WHEN LOWER(DATA_TYPE) IN (N'decimal', N'numeric')
        THEN DATA_TYPE
             + N'(' + CAST(NUMERIC_PRECISION AS NVARCHAR(5))
             + N',' + CAST(NUMERIC_SCALE AS NVARCHAR(5))
             + N')'
      WHEN LOWER(DATA_TYPE) = N'datetime'
        THEN N'datetime2(0)'    -- datetime not supported in Synapse SQL pools :contentReference[oaicite:1]{index=1}
      ELSE DATA_TYPE
    END
    + N' ' 
    + CASE WHEN IS_NULLABLE = 'YES' THEN N'NULL' ELSE N'NOT NULL' END
    + N',' + CHAR(13) + CHAR(10)
  FROM Cols;

  --
  -- Trim the trailing comma, close the CREATE, and execute it
  --
  SET @DDL = LEFT(@DDL, LEN(@DDL) - 3) + CHAR(13) + CHAR(10) + N');';
  EXEC sp_executesql @DDL;
END