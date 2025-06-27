CREATE PROCEDURE [dbo].[InsertSFTPFolderData]
   ( @JsonData NVARCHAR(MAX))
AS
BEGIN


    DECLARE @MaxFolderName VARCHAR(10);

    BEGIN TRY
        -- Debug: Print received JSON for verification
        PRINT 'Received JSON: ' + @JsonData;

		--Truncate table before loading
		TRUNCATE TABLE dbo.SFTPFolder

        -- Insert JSON data into the SFTPFolder table
        INSERT INTO dbo.SFTPFolder (FolderName, FolderType)
        SELECT 
            -- Convert 'DD-MM-YYYY' format to DATE
            TRY_CONVERT(DATE, folders.name, 105) AS FolderName, 
            folders.type AS FolderType
        FROM OPENJSON(@JsonData)  -- No path required since ADF sends a direct array
        WITH (
            name NVARCHAR(50),
            type NVARCHAR(20)
        ) AS folders;

        PRINT 'Data inserted successfully';

		select @MaxFolderName= FORMAT(MAX(FolderName), 'dd-MM-yyyy') FROM dbo.SFTPFolder;
		select @MaxFolderName as FolderName
    END TRY
    BEGIN CATCH
        PRINT 'Error: ' + ERROR_MESSAGE();
    END CATCH
END;