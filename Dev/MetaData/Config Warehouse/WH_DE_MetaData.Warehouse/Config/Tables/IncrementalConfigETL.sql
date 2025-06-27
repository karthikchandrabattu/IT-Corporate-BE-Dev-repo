CREATE TABLE [Config].[IncrementalConfigETL] (

	[ConfigId] int NOT NULL, 
	[DBSourceName] varchar(max) NOT NULL, 
	[SourceDBName] varchar(max) NOT NULL, 
	[SourceSchemaName] varchar(max) NULL, 
	[SourceTableName] varchar(max) NULL, 
	[BronzeSchemaName] varchar(max) NULL, 
	[BronzeTableName] varchar(max) NULL, 
	[SilverSchemaName] varchar(max) NULL, 
	[SilverTableName] varchar(max) NULL, 
	[GoldSchemaName] varchar(max) NULL, 
	[GoldTableName] varchar(max) NULL, 
	[PrimaryKey] varchar(max) NULL, 
	[IsFullLoad] int NOT NULL, 
	[WaterMarkField] varchar(max) NULL, 
	[WaterMarkValue] varchar(max) NULL, 
	[IsActive] int NOT NULL, 
	[SourceQuery] varchar(max) NULL, 
	[SourceSystem] varchar(max) NOT NULL
);