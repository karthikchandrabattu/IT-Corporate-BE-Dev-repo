CREATE PROCEDURE [dbo].[BuildSelectQueryFromJson]
  @rawSql   NVARCHAR(MAX),
  @colsJson NVARCHAR(MAX)
AS
BEGIN
  SET NOCOUNT ON;

  DECLARE 
    @colsList NVARCHAR(MAX),
    @finalSql NVARCHAR(MAX),
    @invalid  NVARCHAR(20) = ' /,;{}()' + CHAR(9) + CHAR(10) + CHAR(13);

  SELECT
    @colsList = STRING_AGG(
      CAST(
        QUOTENAME(COLUMN_NAME)
        + ' AS '
        + QUOTENAME(
            TRANSLATE(
              COLUMN_NAME,
              @invalid,
              REPLICATE('_', LEN(@invalid))
            )
          )
      AS NVARCHAR(MAX))  -- ← force MAX here
    , ', ')
  FROM OPENJSON(@colsJson)
    WITH (COLUMN_NAME NVARCHAR(255) '$.COLUMN_NAME');

  SET @finalSql = REPLACE(
    @rawSql,
    'SELECT *',
    'SELECT ' + @colsList
  );

  SELECT @finalSql AS CleanQuery;
END;