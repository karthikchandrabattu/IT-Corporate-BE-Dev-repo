CREATE TABLE [Config].[Temp] (

	[ConfigId] bigint NULL, 
	[DBSourceName] varchar(max) NULL, 
	[SourceDBName] varchar(max) NULL, 
	[SourceSchemaName] varchar(max) NULL, 
	[SourceTableName] varchar(max) NULL, 
	[BronzeSchemaName] varchar(max) NULL, 
	[BronzeTableName] varchar(max) NULL, 
	[SilverSchemaName] varchar(max) NULL, 
	[SilverTableName] varchar(max) NULL, 
	[GoldSchemaName] varchar(max) NULL, 
	[GoldTableName] varchar(max) NULL, 
	[PrimaryKey] varchar(max) NULL, 
	[IsFullLoad] varchar(max) NULL, 
	[WaterMarkField] varchar(max) NULL, 
	[WaterMarkValue] varchar(max) NULL, 
	[IsActive] bigint NULL, 
	[SourceQuery] varchar(max) NULL, 
	[SourceSystem] varchar(max) NULL
);