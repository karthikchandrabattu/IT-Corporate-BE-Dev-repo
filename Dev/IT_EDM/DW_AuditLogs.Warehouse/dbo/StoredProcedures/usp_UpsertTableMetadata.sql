CREATE   PROCEDURE dbo.usp_UpsertTableMetadata
  @TableName       NVARCHAR(255),
  @PKCols          NVARCHAR(MAX),
  @FKJson          NVARCHAR(MAX)
AS
BEGIN
  SET NOCOUNT ON;

  IF EXISTS (SELECT 1 FROM dbo.Metadata_TableList WHERE SourceTableName = @TableName)
  BEGIN
    UPDATE dbo.Metadata_TableList
    SET 
      KeyColumnList   = @PKCols,
      ForeignKeyList  = @FKJson
    WHERE SourceTableName = @TableName;
  END
  ELSE
  BEGIN
    INSERT dbo.Metadata_TableList
      (SourceTableName, KeyColumnList, ForeignKeyList)
    VALUES
      (@TableName, @PKCols, @FKJson);
  END
END;