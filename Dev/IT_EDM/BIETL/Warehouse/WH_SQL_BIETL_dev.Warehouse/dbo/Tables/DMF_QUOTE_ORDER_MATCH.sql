CREATE TABLE [dbo].[DMF_QUOTE_ORDER_MATCH] (

	[QUOTE_LINE_KEY] int NULL, 
	[REASON] varchar(8000) NULL, 
	[CREATE_STAMP] datetime2(6) NULL, 
	[CALLED_FROM] varchar(8000) NULL, 
	[ORDER_NO] varchar(8000) NULL, 
	[SHIP_KEY] bigint NULL, 
	[MFR] varchar(8000) NULL, 
	[MPN] varchar(8000) NULL, 
	[FPN] varchar(8000) NULL, 
	[CPN] varchar(8000) NULL, 
	[QUANTITY] int NULL, 
	[RESALE] decimal(12,6) NULL, 
	[EXCH_RATE_TO_US] decimal(10,6) NULL, 
	[RESALE_USD] decimal(23,12) NULL, 
	[CURRENCY] varchar(8000) NULL, 
	[ORDER_DATE] datetime2(6) NULL, 
	[REQUIRED_DATE] datetime2(6) NULL, 
	[INVOICE_DATE] varchar(8000) NULL, 
	[PMCATEGORY_KEY] int NULL
);