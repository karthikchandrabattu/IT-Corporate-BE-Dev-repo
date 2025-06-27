CREATE TABLE [dbo].[DMA_AUTO_QUOTE_STATS_MONTHLY] (

	[AsOfDate] datetime2(6) NULL, 
	[FISCAL_MONTH_KEY] int NULL, 
	[PMCATEGORY_KEY] bigint NULL, 
	[Original_Subline_Value] varchar(8000) NULL, 
	[Group] varchar(8000) NULL, 
	[Category] varchar(8000) NULL, 
	[Description] varchar(8000) NULL, 
	[Subline_Quoted] varchar(8000) NULL, 
	[Quote_Source] varchar(8000) NULL, 
	[BID_or_BUY] varchar(8000) NULL, 
	[DollarValue] decimal(38,6) NULL, 
	[Lines] int NULL, 
	[FMDays] int NULL, 
	[LastCompleteStamp] datetime2(6) NULL
);