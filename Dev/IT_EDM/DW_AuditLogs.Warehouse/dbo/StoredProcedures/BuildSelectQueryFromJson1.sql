CREATE   PROCEDURE [dbo].[BuildSelectQueryFromJson1]
  @rawSql   NVARCHAR(MAX),
  @colsJson NVARCHAR(MAX)
AS
BEGIN
  SET NOCOUNT ON;

  DECLARE 
    @colsList NVARCHAR(MAX),
    @finalSql NVARCHAR(MAX),
    @invalid  NVARCHAR(20) = ' /,;{}()' 
                        + CHAR(9)  -- tab
                        + CHAR(10) -- line feed
                        + CHAR(13) -- carriage return
    ;

  -- 1) Build LIST of: [OriginalName] AS [Sanitized_Name]
  SELECT
    @colsList = STRING_AGG(
      QUOTENAME(COLUMN_NAME)
      + ' AS '
      + QUOTENAME(
          TRANSLATE(
            COLUMN_NAME,
            @invalid,
            REPLICATE('_', LEN(@invalid))
          )
        )
    , ', ')
  FROM OPENJSON(@colsJson)
    WITH (COLUMN_NAME NVARCHAR(255) '$.COLUMN_NAME');

  -- 2) Replace the SELECT * in your raw SQL
  SET @finalSql = REPLACE(
    @rawSql,
    'SELECT *',
    'SELECT ' + @colsList
  );

  -- 3) Return the cleaned query
  SELECT @finalSql AS CleanQuery;
END;