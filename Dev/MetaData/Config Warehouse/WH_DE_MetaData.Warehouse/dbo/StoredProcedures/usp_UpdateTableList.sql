CREATE   PROCEDURE usp_UpdateTableList
@ConfigIdList VARCHAR(255)
AS
BEGIN

IF @ConfigIdList IS NOT NULL
BEGIN
    -- Remove the double quotes
    SET @ConfigIdList = REPLACE(@ConfigIdList, '"', '');

    -- Update records where ConfigId is in the split list
    UPDATE [WH_DE_MetaData].[Config].[MetaETL]
    SET IsActive = 0
    WHERE ConfigId IN (
        SELECT TRY_CAST(value AS INT)
        FROM STRING_SPLIT(@ConfigIdList, ',')
        WHERE TRY_CAST(value AS INT) IS NOT NULL
    );
END
END