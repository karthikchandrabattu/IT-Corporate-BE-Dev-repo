CREATE PROCEDURE dbo.usp_SyncMetadata
  @PKJson NVARCHAR(MAX),   -- pass: @string(activity('GetPKs').output.value)
  @FKJson NVARCHAR(MAX)    -- pass: @string(activity('GetFKs').output.value)
AS
BEGIN
  SET NOCOUNT ON;

  ----------------------------------------------------------------
  -- 1) UPDATE existing Primary Keys
  ----------------------------------------------------------------
  ;WITH JSONPK AS (
    SELECT 
      TableName,
      PKCols
    FROM OPENJSON(@PKJson)
    WITH (
      TableName NVARCHAR(255) '$.TableName',
      PKCols     NVARCHAR(MAX) '$.PKCols'
    )
  )
  UPDATE M
  SET KeyColumnList = J.PKCols
  FROM dbo.Metadata_TableList AS M
  JOIN JSONPK               AS J
    ON M.SourceTableName = J.TableName;

  ----------------------------------------------------------------
  -- 2) INSERT missing Primary Keys
  ----------------------------------------------------------------
  INSERT INTO dbo.Metadata_TableList (SourceTableName, KeyColumnList)
  SELECT 
    J.TableName,
    J.PKCols
  FROM OPENJSON(@PKJson)
  WITH (
    TableName NVARCHAR(255) '$.TableName',
    PKCols     NVARCHAR(MAX) '$.PKCols'
  )           AS J
  WHERE NOT EXISTS (
    SELECT 1
    FROM dbo.Metadata_TableList M2
    WHERE M2.SourceTableName = J.TableName
  );

  ----------------------------------------------------------------
  -- 3) UPDATE existing Foreign Keys
  ----------------------------------------------------------------
  ;WITH JSONFK AS (
    SELECT 
      ChildTable,
      ChildColumn,
      ParentTable,
      ParentColumn
    FROM OPENJSON(@FKJson)
    WITH (
      ChildTable   NVARCHAR(255) '$.ChildTable',
      ChildColumn  NVARCHAR(255) '$.ChildColumn',
      ParentTable  NVARCHAR(255) '$.ParentTable',
      ParentColumn NVARCHAR(255) '$.ParentColumn'
    )
  )
  UPDATE F
  SET 
    ParentTable  = J.ParentTable,
    ParentColumn = J.ParentColumn
  FROM dbo.Metadata_FK AS F
  JOIN JSONFK            AS J
    ON F.ChildTable  = J.ChildTable
   AND F.ChildColumn = J.ChildColumn;

  ----------------------------------------------------------------
  -- 4) INSERT missing Foreign Keys
  ----------------------------------------------------------------
  INSERT INTO dbo.Metadata_FK
    (ChildTable, ChildColumn, ParentTable, ParentColumn)
  SELECT 
    J.ChildTable,
    J.ChildColumn,
    J.ParentTable,
    J.ParentColumn
  FROM OPENJSON(@FKJson)
  WITH (
    ChildTable   NVARCHAR(255) '$.ChildTable',
    ChildColumn  NVARCHAR(255) '$.ChildColumn',
    ParentTable  NVARCHAR(255) '$.ParentTable',
    ParentColumn NVARCHAR(255) '$.ParentColumn'
  )           AS J
  WHERE NOT EXISTS (
    SELECT 1
    FROM dbo.Metadata_FK F2
    WHERE F2.ChildTable  = J.ChildTable
      AND F2.ChildColumn = J.ChildColumn
  );
END;