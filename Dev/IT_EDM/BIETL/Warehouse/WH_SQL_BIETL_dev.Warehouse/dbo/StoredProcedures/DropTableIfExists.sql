CREATE   PROCEDURE dbo.DropTableIfExists
  @SchemaName SYSNAME,
  @TableName  SYSNAME
AS
BEGIN
  SET NOCOUNT ON;

  DECLARE 
    @FullName NVARCHAR(517) = QUOTENAME(@SchemaName) + N'.' + QUOTENAME(@TableName),
    @Dropped  BIT           = 0;

  IF OBJECT_ID(@FullName,'U') IS NOT NULL
  BEGIN
    EXEC(N'DROP TABLE ' + @FullName);
    SET @Dropped = 1;
  END

  SELECT 
    @SchemaName AS SchemaName,
    @TableName  AS TableName,
    CASE WHEN @Dropped = 1 THEN 'Dropped' ELSE 'NotFound' END AS Status;
END;