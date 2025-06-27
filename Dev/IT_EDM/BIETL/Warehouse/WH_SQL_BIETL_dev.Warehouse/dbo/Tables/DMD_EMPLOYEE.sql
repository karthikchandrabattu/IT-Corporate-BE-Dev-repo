CREATE TABLE [dbo].[DMD_EMPLOYEE] (

	[EMPLOYEE_KEY] bigint NULL, 
	[Employee_Number] varchar(8000) NULL, 
	[NTAccount] varchar(8000) NULL, 
	[DisplayName] varchar(8000) NULL, 
	[EMail] varchar(8000) NULL, 
	[DepartmentID] varchar(8000) NULL, 
	[DepartmentName] varchar(8000) NULL, 
	[Title] varchar(8000) NULL, 
	[Branch] varchar(8000) NULL, 
	[EmployeeType] varchar(8000) NULL, 
	[TerminationDate] datetime2(6) NULL, 
	[Supervisor_NTAccount] varchar(8000) NULL
);