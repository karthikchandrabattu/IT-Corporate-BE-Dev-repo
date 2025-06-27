CREATE   PROCEDURE [dbo].[usp_GetListOfFiles]
AS
BEGIN
    WITH CTE AS (
        SELECT 
            sf.FolderName, 
            ROW_NUMBER() OVER (PARTITION BY sf.FolderName ORDER BY COALESCE(fa.Status, '')) AS rn
        FROM [dbo].[SFTPFolder] sf
        LEFT JOIN [dbo].[FileProcessAudit] fa
            ON CAST(FORMAT(sf.FolderName, 'dd-MM-yyyy') AS VARCHAR(255)) = fa.FolderName -- Simplified join condition
        WHERE fa.FolderName IS NULL OR fa.Status = 'FAILURE'
    )
    SELECT FolderName 
    FROM CTE 
    WHERE rn = 1
    ORDER BY FolderName;
END;