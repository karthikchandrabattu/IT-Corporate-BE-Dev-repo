CREATE PROCEDURE [dbo].[usp_UpdateMetadataActiveStatus]
    @JsonData NVARCHAR(MAX)
AS
BEGIN
    BEGIN TRY
        -- Reset all IsActive flags before reactivating relevant ones
        UPDATE Metadata_TableList
        SET IsActive = 0;

        -- Set IsActive = 1 for tables matching today's ready list
        UPDATE M
        SET IsActive = 1
        FROM Metadata_TableList M
        JOIN OPENJSON(@JsonData)
        WITH (
            DataSource NVARCHAR(200)
        ) AS J
            ON M.SourceTableName = PARSENAME(J.DataSource, 1)
           AND M.SourceSchemaName = PARSENAME(J.DataSource, 2)
        WHERE CAST(ISNULL(M.ETLRefresh_Timestamp, '1900-01-01') AS DATE) < CAST(GETDATE() AS DATE);
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;