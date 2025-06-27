CREATE PROCEDURE [dbo].[GetDynamicSelectQuery]
    @TableName           VARCHAR(255),
    @StartDate           DATETIME,
    @EndDate             DATETIME,
    @LoadType            VARCHAR(30),
    @IsFullLoadRequired  BIT = 0
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @SQL            NVARCHAR(MAX);
    DECLARE @FilterColumn   VARCHAR(300);
    DECLARE @FilterColumn2  VARCHAR(300);
    DECLARE @Schema         VARCHAR(100);

    SELECT 
        @Schema = SourceSchemaName,
        @FilterColumn = CASE 
                            WHEN CHARINDEX(',', FilterColumnName) > 0
                                THEN LEFT(FilterColumnName, CHARINDEX(',', FilterColumnName) - 1)
                            ELSE FilterColumnName
                        END,
        @FilterColumn2 = CASE
                            WHEN CHARINDEX(',', FilterColumnName) > 0
                                THEN LTRIM(RIGHT(FilterColumnName, LEN(FilterColumnName) - CHARINDEX(',', FilterColumnName)))
                            ELSE NULL
                        END
    FROM dbo.Metadata_TableList
    WHERE SourceTableName = @TableName;

    SET @Schema = ISNULL(@Schema, 'dbo');

    IF (@LoadType = 'Full' OR @IsFullLoadRequired = 1)
    BEGIN
        SET @SQL = 'SELECT * FROM [' + @Schema + '].[' + @TableName + ']';
    END
    ELSE IF (@LoadType = 'Incremental' AND @IsFullLoadRequired = 0)
    BEGIN
        IF @FilterColumn2 IS NOT NULL
        BEGIN
            SET @SQL = 'SELECT * FROM [' + @Schema + '].[' + @TableName + '] ' +
                       'WHERE [' + @FilterColumn + '] BETWEEN ''' + CONVERT(NVARCHAR(30), @StartDate, 120) + ''' AND ''' + CONVERT(NVARCHAR(30), @EndDate, 120) + ''' ' +
                       'OR [' + @FilterColumn2 + '] BETWEEN ''' + CONVERT(NVARCHAR(30), @StartDate, 120) + ''' AND ''' + CONVERT(NVARCHAR(30), @EndDate, 120) + '''';
        END
        ELSE IF @FilterColumn IS NOT NULL
        BEGIN
            SET @SQL = 'SELECT * FROM [' + @Schema + '].[' + @TableName + '] ' +
                       'WHERE [' + @FilterColumn + '] BETWEEN ''' + CONVERT(NVARCHAR(30), @StartDate, 120) + ''' AND ''' + CONVERT(NVARCHAR(30), @EndDate, 120) + '''';
        END
        ELSE
        BEGIN
            SET @SQL = '-- No filter column defined in metadata for incremental load.';
        END
    END
    ELSE
    BEGIN
        SET @SQL = '-- Invalid LoadType or missing metadata.';
    END

    SELECT @SQL AS SelectQuery;
END