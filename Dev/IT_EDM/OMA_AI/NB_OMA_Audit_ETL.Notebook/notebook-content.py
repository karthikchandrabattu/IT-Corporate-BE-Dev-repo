# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "d7565994-cfa7-425f-83a1-7cbd9b17b177",
# META       "default_lakehouse_name": "LH_OMA_AI",
# META       "default_lakehouse_workspace_id": "396e8831-ce18-4879-8649-afb3202741fe",
# META       "known_lakehouses": [
# META         {
# META           "id": "5677ae72-a852-4cf5-bebf-d7174c1589c0"
# META         },
# META         {
# META           "id": "d7565994-cfa7-425f-83a1-7cbd9b17b177"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

df = spark.read.format("csv").option("header","true").load("Files/OMA_AUDIT_DATA.csv")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = df.withColumnRenamed("Approved (Y/N?)", "Approved")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.write.format("delta").save("abfss://eb87c50a-8bc7-40f8-bb1a-8a135398c6f4@onelake.dfs.fabric.microsoft.com/5677ae72-a852-4cf5-bebf-d7174c1589c0/Tables/OMA_AUDIT_DATA")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.write.format("delta").save("abfss://396e8831-ce18-4879-8649-afb3202741fe@onelake.dfs.fabric.microsoft.com/d7565994-cfa7-425f-83a1-7cbd9b17b177/Tables/OMA_AUDIT_DATA")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col, count

duplicates_df = df.groupBy(df.columns) \
                  .count() \
                  .filter("count > 1")

duplicates_df.show(truncate=False)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED

DECLARE @Today DateTime = CONVERT(Varchar(10),getdate(),121)
DECLARE @TodayMinus13Months DateTime = DATEADD(MONTH, -13, @Today)

SELECT CASE WHEN RIGHT(AC.MFRX_CODE,1) IN ('4','9') THEN 'FGC' ELSE GroupNTDesc END AS BusinessUnit, AC.Cmpy_Code,Bill_Cust,Ship_Cust,Bill_Cust + Ship_Cust AS Shipto,Ordr_Noxx,Invc_Noxx,Line_Noxx,AC.ORDR_DATE,
CASE WHEN ISNULL(Approved,0) = 1 THEN 'Y' ELSE 'N' END AS Approved,ApprovedByAccount,ApprovedByFullName
,Comment,ApprovedDate,MFRX_CODE,REQD_QTYX,SHIP_QTYX,AssignedToAccount,AssignedToFullName,AvgCostUSD,HistoricalAvgCostUSD,AC.Resale,Currency,ExRate,AuthCode,SSDCost,SSDCostCurr
,SSDCostExRate,SSDCostUSD,ASSUMEDSSDCost,ASSUMEDSSDCostUSD,AC.GP,ProgrammingCost,CostOverride,Guid_noxx,
(
    SELECT STUFF((
        SELECT ',' + CAST(innerAC.IDActionCode AS VARCHAR(20))
        FROM OrderEntryLive.dbo.CboXActionCodes innerAC
        WHERE innerAC.Guid_noxx = AC.Guid_noxx
		  AND innerAC.Cmpy_Code = AC.Cmpy_Code
        FOR XML PATH(''), TYPE).value('.', 'VARCHAR(500)'), 1, 1, '')
) AS ActionCodes_Combined,
INV.FPN,INV.MPN,OEBODT_CUST_PART AS CPN,INV.ITEMNO,INV.CLASS,
OEBOHD_BILL_TYPE AS BILLTYPE,
OEBODT.REQD_DATE,
OEBODT.COMI_DATE AS COMMIT_DATE,
OEBODT_UNIT_PRIC AS CBO_VALUE,
OEBODT_UNIT_COST AS CBO_COST,
INV.MFR,
OEBODT_REGS_PART AS REG_NUM,
OEBODT_REGS_FLAG AS REG_FLAG,
OEBODT_ASSO_QUOT_NOXX AS [CBO_QUOTENO/QUOTENO],
OEBODT_ASSO_QUOT_CUST_LINE AS [CBO_QUOTELN/QUOTE_LINE],
INV.POQ AS MOQ,
INV.MPQ,
Stock AS Stock_Qty,
INV.ATS AS ATS_Qty,
PBOSupplier AS PBO_Qty,
CBO AS CBO_Qty,
AvgCost,
LastCost,
AlgoCode,
ProductTypeCode AS ProductType_Code,
INV.LeadTime,
RedFlag AS Alert_Flag,
INV.RegisteredPart,
CUBILL_PAYM_TERM AS TERMS,
CUBILL_CRED_WTCH AS CREDIT_WATCH,
CUSHIP_CUST_TYPE AS Cust_Type,
CCV.ATGENP_DESC_XXXX AS Cust_Type_Description,
CUSHIP_PROG_TYPE AS Cust_Program_Type,
MRKT_SEGM AS Cust_Market_Segment,
[HTSCode] AS [HTS CODE],
[HTSCodeTariffRate] as [HTS CODE TARIFF RATE],
[TariffCountryOfOrigin] as COO,
ICO.ATGENP_DESC_XXXX AS [SHIPTO COUNTRY],
QSL.ResalePrice AS [Quote Resale USD],
QuoteCompleteStamp AS [Quote Complete Date],
CostDescription AS Quoted_Cost_Category
  FROM OrderEntryLive.dbo.CboXActionCodes AC
		CROSS APPLY (
			SELECT OEBODT_CMPY_CODE, OEBODT_ITEM_NOXX,OEBOHD_BILL_TYPE, OEBODT.REQD_DATE, OEBODT.COMI_DATE, OEBODT_UNIT_PRIC, OEBODT_UNIT_COST,
				   OEBODT_REGS_PART,OEBODT_REGS_FLAG,OEBODT_ASSO_QUOT_NOXX,OEBODT_ASSO_QUOT_CUST_LINE, OEBODT_CUST_PART, OEBODT_PROJ_NOXX, OEBODT_ASSO_SLIN_NOXX,
				   OEBODT_ENDX_CUST_CMPY,OEBODT_ENDX_CUST_NOXX, OEBODT_CLAS_CODE
			  FROM DatawhseLive.dbo.OEBODTFL OEBODT
				INNER JOIN DatawhseLive.dbo.OEBOHDFL
				ON	OEBOHD_CMPY_CODE = OEBODT_CMPY_CODE
				AND OEBOHD_BILL_CUST = OEBODT_BILL_CUST
				AND OEBOHD_SHIP_CUST = OEBODT_SHIP_CUST
				AND OEBOHD_ORDR_NOXX = OEBODT_ORDR_NOXX
				AND OEBOHD_INVC_NOXX = OEBODT_INVC_NOXX
			  WHERE OEBODT_GUID_NOXX = Guid_noxx
			    AND OEBODT_CMPY_CODE = Cmpy_Code	
			UNION
			SELECT OETRDT_CMPY_CODE, OETRDT_ITEM_NOXX, OETRDT_BILL_TYPE, OETRDT.REQD_DATE, OETRDT.COMI_DATE, OETRDT_UNIT_PRIC, OETRDT_UNIT_COST,
				   OETRDT_REGS_PART,OETRDT_REGS_FLAG,OETRDT_ASSO_QUOT_NOXX,OETRDT_ASSO_QUOT_CUST_LINE, OETRDT_CUST_PART, OETRDT_PROJ_NOXX, OETRDT_ASSO_SLIN_NOXX,
				   OETRDT_ENDX_CUST_CMPY,OETRDT_ENDX_CUST_NOXX, OETRDT_CLAS_CODE
			  FROM DatawhseLive.dbo.vwOETRDTFL OETRDT
				INNER JOIN DatawhseLive.dbo.vwOETRHDFL
				ON  OETRHD_CMPY_CODE = OETRDT_CMPY_CODE
				AND OETRHD_BILL_CUST = OETRDT_BILL_CUST
				AND OETRHD_SHIP_CUST = OETRDT_SHIP_CUST
				AND OETRHD_ORDR_NOXX = OETRDT_ORDR_NOXX
				AND OETRHD_INVC_NOXX = OETRDT_INVC_NOXX
			 WHERE OETRDT_CMPY_CODE = AC.Cmpy_Code
			   AND OETRDT_BILL_CUST = AC.Bill_Cust
			   AND OETRDT_SHIP_CUST = AC.Ship_cust
			   AND OETRDT_ORDR_NOXX = AC.Ordr_Noxx
			   AND OETRDT_INVC_NOXX = AC.Invc_Noxx
			   AND OETRDT_LINE_NOXX = AC.Line_Noxx
		) OEBODT
		INNER JOIN PMIQ.dbo.PMIQDetailFutView INV
		ON  OEBODT_CMPY_CODE = INV.Company
		AND OEBODT_ITEM_NOXX = INV.ItemNo
		INNER JOIN DatawhseLive.dbo.CUBILLFL
		ON	CUBILL_CMPY_CODE = AC.Cmpy_Code
		AND CUBILL_BILL_CUST = AC.Bill_Cust
		INNER JOIN DatawhseLive.dbo.CUSHIPFL
		ON  CUSHIP_CMPY_CODE = AC.Cmpy_Code
		AND CUSHIP_BILL_CUST = AC.Bill_Cust
		AND CUSHIP_SHIP_CUST = AC.Ship_Cust
		INNER JOIN  Datawhse.dbo.ATGENPFL ICO
		ON	ICO.ATGENP_CMPY_CODE = CUSHIP_CMPY_CODE
		AND ICO.ATGENP_MAIN_CODE = 'ICO'
		AND ICO.ATGENP_SUBX_CODE = CUSHIP_CTRY_CODE
		INNER JOIN CorporateQuote.dbo.BUxClass B
		ON  B.Company = OEBODT_CMPY_CODE
		AND B.Class = OEBODT_CLAS_CODE
		INNER JOIN CorporateQuote.dbo.Groups G
		ON  B.Company = G.Company
		AND B.BU = G.GID
		LEFT OUTER JOIN Datawhse.dbo.ATGENPFL CCV
		ON	CCV.ATGENP_CMPY_CODE = CUSHIP_CMPY_CODE
		AND CCV.ATGENP_MAIN_CODE = 'CCV'
		AND CCV.ATGENP_SUBX_CODE = CUSHIP_CUST_TYPE
		LEFT OUTER JOIN [DataWhse].[dbo].[TariffParts] TP
		ON  TP.Company = INV.Company
		AND TP.ItemNo = INV.ItemNo
		AND PRIMARY_PART = 'Y'
		LEFT OUTER JOIN Datawhse.dbo.TSMHeader TH
		ON	TH.CMPY_CODE = OEBODT_CMPY_CODE
		AND PROJ_NOXX = OEBODT_PROJ_NOXX
		OUTER APPLY (
			SELECT QSL.ResalePrice, QL.QuoteCompleteStamp, CostDescription
		      FROM CorporateQuote.dbo.QuoteSubLineView QSL
				INNER JOIN CorporateQuote.dbo.QuoteLineView QL
				ON  QL.QuoteNo = QSL.QuoteNo
				AND QL.QuoteLineNo = QSL.QuoteLineNo
				LEFT OUTER JOIN CorporateQuote.dbo.QuoteCostType QCT
				ON	QSL.CostType = QCT.CostType
			 WHERE QSL.QuoteNo = OEBODT_ASSO_QUOT_NOXX
			   AND QSL.QuoteLineNo = OEBODT_ASSO_QUOT_CUST_LINE
			   AND QSL.QuoteSubLineNo = OEBODT_ASSO_SLIN_NOXX
		) QSL
 WHERE AC.ORDR_DATE >= @TodayMinus13Months

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(duplicates_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

duplicates_df.count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_deduped = df.dropDuplicates()
df_deduped.count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df1 = spark.read.format("csv").option("header","true").load("Files/AUDIT_DATA.csv")


duplicates_df1 = df1.groupBy(df1.columns) \
                  .count() \
                  .filter("count > 1")

duplicates_df1.count()

df_deduped1 = df1.dropDuplicates()

df_deduped1.count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

duplicates_df1.count()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col

df_transformed = df.withColumnRenamed("CBO_QUOTENO/QUOTENO", "CBO_QUOTENO") \
                   .withColumnRenamed("CBO_QUOTELN/QUOTE_LINE", "CBO_QUOTELN")

columns_to_drop = [
    "COO",
    "SHIPTO_COUNTRY",
    "ActionCodesReason_Combined",
    "ActionCodesDesc_Combined"
]
for col_name in columns_to_drop:
    if col_name in df_transformed.columns:
        df_transformed = df_transformed.drop(col_name)

expected_columns = [ "BusinessUnit", "Cmpy_Code", "Bill_Cust", "Ship_Cust", "Shipto", "Ordr_Noxx", "Invc_Noxx", "Line_Noxx",
    "ORDR_DATE", "Approved (Y/N?)", "ApprovedByAccount", "ApprovedByFullName", "Comment", "Approved_Date",
    "MFRX_CODE", "REQD_QTYX", "SHIP_QTYX", "AssignedToAccount", "AssignedToFullName", "AvgCostUSD",
    "HistoricalAvgCostUSD", "Resale", "Currency", "ExRate", "AuthCode", "SSDCost", "SSDCostCurr", "SSDCostExRate",
    "SSDCostUSD", "ASSUMEDSSDCost", "ASSUMEDSSDCostUSD", "GP", "ProgrammingCost", "CostOverride", "Guid_noxx",
    "ActionCodes_Combined", "FPN", "MPN", "CPN", "ITEMNO", "CLASS", "MFR", "BILLTYPE", "REQD_DATE", "COMMIT_DATE",
    "CBO_VALUE", "CBO_COST", "POS", "BE_COST", "REG_NUM", "REG_FLAG", "CBO_QUOTENO", "CBO_QUOTELN", "MOQ", "MPQ",
    "Stock_Qty", "ATS_Qty", "PBO_Qty", "CBO_Qty", "AvgCost", "LastCost", "AlgoCode", "ProductType_Code", "LeadTime",
    "Alert_Flag", "RegisteredPart", "Last_Quote_Date", "Last_Quoted_Price", "Quoted_Cost_Category", "TERMS",
    "CREDIT_WATCH", "Cust_Type", "Cust_Type_Description", "Cust_Program_Type", "Cust_Market_Segment", "HTS_CODE",
    "HTS_CODE_TARIFF_RATE"
]

final_df = df_transformed.select([col(c) for c in expected_columns if c in df_transformed.columns])

final_df.printSchema()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
