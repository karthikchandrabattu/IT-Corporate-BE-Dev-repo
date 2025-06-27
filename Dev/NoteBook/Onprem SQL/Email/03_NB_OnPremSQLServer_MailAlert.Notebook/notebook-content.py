# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "a6720a25-5d7d-4636-811e-880533861456",
# META       "default_lakehouse_name": "KH_LH_Silver",
# META       "default_lakehouse_workspace_id": "27123242-df72-41f7-822b-0b14db152c20",
# META       "known_lakehouses": [
# META         {
# META           "id": "a6720a25-5d7d-4636-811e-880533861456"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # _**Mail Activity**_

# CELL ********************

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import (
col, lit, concat, when, trim, collect_list, row_number, to_date,date_format,
col, concat, lit, to_timestamp, date_format, to_date, coalesce,concat_ws, md5,
udf , concat, to_timestamp,count, when )
from pyspark.sql.window import Window
from datetime import datetime, timezone, timedelta
from delta.tables import DeltaTable
import pandas as pd
from com.microsoft.spark.fabric import Constants
import com.microsoft.spark.fabric
from com.microsoft.spark.fabric.Constants import Constants
from pyspark.sql.types import (
    DoubleType, IntegerType, BooleanType, StringType,StructField,ArrayType,
    BinaryType, TimestampType, DateType, LongType, StructType
)
import concurrent.futures
import pytz
import traceback
import os
from pyspark.sql import functions as F
from pyspark.sql.types import StringType
import re
import json

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


recipient_email = """email"""
subject= f"""Fabric Pipeline Alert: Table Load Failures Detected"""


content = ["I hope this message finds you well. Our monitoring system has identified a problem with some tables in the Fabric environment that needs your attention.",
"As part of our routine system monitoring, we detected that some tables is failing to load correctly. A preview of the impacted data is provided below."]

message = f"""<div class="alert-box" style="border-left: 4px solid #dc2626;background-color: #fee2e2;">
            <div class="alert-icon" style="color: #b91c1c;">⚠️</div>
            <div class="alert-text" style="color: #991b1b;">
                <strong>Processing Error:</strong> Data integrity issues detected.
            </div>
        </div> """

    

email_body = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Pipeline Notification</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Roboto', Arial, sans-serif;
            line-height: 1.6;
            color: #1e293b;
            background-color: #f1f5f9;
            padding: 20px;
            margin: 0;
        }}

        .email-container {{
            max-width: 650px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
        }}

        .batch-report-section {{
            margin-bottom: 10px;
        }}
        
        .info-tablet {{
            display: inline-block;
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            overflow: hidden;
            max-width: 500px;
        }}
        
        .info-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .info-table tr:first-child td {{
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .info-label {{
            padding: 10px 15px;
            font-size: 14px;
            font-weight: 600;
            color: #000000;
            background-color: #cecece;
            border-right: 1px solid #e2e8f0;
            white-space: nowrap;
        }}
        
        .info-value-cell {{
            padding: 10px 20px;
            font-size: 15px;
            font-weight: 500;
            color: #0f172a;
            background-color: #ffffff;
        }}
        
        .email-header {{
            background: #f1f5f9;
            padding: 25px 40px;
            text-align: center;
            position: relative;
            border-bottom-left-radius: 30% 15%;
            border-bottom-right-radius: 30% 15%;
        }}

        .company-logo {{
            max-height: 100px;
            filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.3));
            animation: logoFloat 6s ease-in-out infinite;
        }}

        .futureelectronics-logo {{
            max-height: 100px;
            filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.3));
            animation: logoFloat 6s ease-in-out infinite;
        }}

        .email-body {{
            padding: 35px;
            position: relative;
            z-index: 1;
        }}
        
        .executions-container {{
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            border-left: 4px solid #2563eb;
            border-radius: 8px;
            padding: 16px 24px;
            margin-bottom: 30px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            animation: fadeSlideDown 0.7s ease-out;
        }}
        
        .executions-row {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 20px;
        }}

        .metadata-item {{
            display: flex;
            flex-direction: column;
            gap: 5px;
            align-items: center;
            flex: 1;
        }}

        .metadata-label {{
            font-size: 12px;
            color: #475569;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.7px;
            margin-bottom: 3px;
        }}

        .metadata-value-wrapper {{
            position: relative;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 4px;
            border: 1px solid #2563eb;
            height: 34px;
            display: flex;
            align-items: center;
            width: 90px;
        }}

        .metadata-value {{
            font-family: 'Courier New', monospace;
            font-size: 15px;
            font-weight: 600;
            color: #0f172a;
            padding: 4px 12px;
            letter-spacing: 0.5px;
            overflow-x: auto;
            white-space: nowrap;
            display: block;
            scrollbar-width: none;
            width: 100%;
        }}
        
        .count-value {{
            width: 100%;
            text-align: center;
        }}

        .greeting {{
            font-size: 22px;
            font-weight: 500;
            color: #0f172a;
            margin-bottom: 20px;
            animation: fadeSlideUp 0.6s ease-out;
        }}

        .content {{
            font-size: 16px;
            color: #334155;
            margin-bottom: 25px;
            line-height: 1.7;
            animation: fadeIn 0.8s ease-out;
        }}

        .alert-box {{
            padding: 18px 20px;
            margin: 25px 0;
            border-radius: 6px;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 5px rgba(220, 38, 38, 0.15);
            animation: pulse 3s infinite;
        }}

        .alert-icon {{
            margin-right: 15px;
            font-size: 24px;
        }}

        .alert-text {{
            font-weight: 500;
        }}

        .table-container {{
            margin: 30px 0;
            border-radius: 8px;
            max-height: 400px; /* Limit height to enable vertical scrolling */
            overflow-y: auto; /* Enable vertical scrolling */
            overflow-x: auto; /* Enable horizontal scrolling */
            width: 100%;
            border: 1px solid #cbd5e1;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            animation: fadeSlideUp 0.8s ease-out;
            position: relative; /* For sticky headers */
        }}

        .table-container {{
            margin: 30px 0;
            border-radius: 8px;
            max-height: 400px; /* Limit height to enable vertical scrolling */
            overflow-y: auto; /* Enable vertical scrolling */
            overflow-x: auto; /* Enable horizontal scrolling */
            width: 100%;
            border: 1px solid #cbd5e1;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            animation: fadeSlideUp 0.8s ease-out;
            position: relative; /* For sticky headers */
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            min-width: 800px; /* Ensure table is wide enough to require horizontal scrolling */
            table-layout: fixed; /* More predictable layout */
        }}
        
        /* Define specific column widths */
        th:nth-child(2), td:nth-child(2) {{ width: 10%; }} /* TableId */
        th:nth-child(3), td:nth-child(3) {{ width: 10%; }} /* TableName */
        th:nth-child(5), td:nth-child(5) {{ width: 70%; }} /* ErrorMessage - increased width */
        th:nth-child(6), td:nth-child(6) {{ width: 10%; }} /* Layer */

        thead {{
            background-color: #e2e8f0;
        }}

        th {{
            padding: 16px 15px;
            text-align: left;
            font-weight: 600;
            color: #0f172a;
            border-bottom: 2px solid #94a3b8;
            position: sticky; /* Make headers sticky while scrolling */
            top: 0; /* Stick to top while scrolling */
            z-index: 10; /* Ensure headers appear above content */
            background-color: #e2e8f0; /* Same as thead background */
            transition: all 0.3s ease;
        }}

        th:after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 2px;
            background-color: #2563eb;
            transition: width 0.3s ease;
        }}

        th:hover:after {{
            width: 100%;
        }}

        tr {{
            transition: all 0.3s ease;
        }}

        tr:hover {{
            background-color: #f1f5f9 !important;
            transform: translateX(5px);
        }}

        td {{
            padding: 14px 15px;
            border-bottom: 1px solid #cbd5e1;
            color: #334155;
            white-space: nowrap; /* Prevent text wrapping for better horizontal scrolling */
            overflow: hidden;
            text-overflow: ellipsis; /* Show ellipsis for overflowing text */
        }}

        .divider {{
            height: 1px;
            background-color: #cbd5e1;
            margin: 30px 0;
        }}

        .signature {{
            margin-top: 30px;
            font-size: 15px;
            color: #475569;
        }}

        .name {{
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 5px;
        }}

        .position {{
            font-size: 14px;
            color: #475569;
        }}

        .email-footer {{
            background-color: #314569;
            padding: 25px;
            text-align: center;
            font-size: 14px;
            color: #475569;
            border-top: 1px solid #cbd5e1;
        }}

        .contact-info {{
            margin: 15px 0;
        }}

        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        @keyframes fadeSlideUp {{
            from {{
                transform: translateY(20px);
                opacity: 0;
            }}
            to {{
                transform: translateY(0);
                opacity: 1;
            }}
        }}

        @keyframes fadeSlideDown {{
            from {{
                transform: translateY(-10px);
                opacity: 0;
            }}
            to {{
                transform: translateY(0);
                opacity: 1;
            }}
        }}

        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.02); }}
            100% {{ transform: scale(1); }}
        }}

        @keyframes logoFloat {{
            0% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-6px); }}
            100% {{ transform: translateY(0); }}
        }}

        @media only screen and (max-width: 600px) {{
            body {{
                padding: 10px;
            }}
            
            .email-body {{
                padding: 25px 20px;
            }}
            
            .email-header {{
                padding: 20px 0;
            }}
            
            .greeting {{
                font-size: 20px;
            }}
            
            .executions-row {{
                flex-direction: column;
                align-items: stretch;
            }}
            
            .metadata-item {{
                width: 100%;
                max-width: 100%;
                margin-bottom: 10px;
            }}
            
            .metadata-value {{
                width: 100%;
            }}

            .metadata-value-wrapper {{
                width: 100%;
            }}
            
            .email-footer {{
                padding: 20px;
            }}
            
            table {{
                font-size: 12px;
            }}
            
            th, td {{
                padding: 10px 8px;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-container">
    
        <div class="email-header"> 
        </div>
        
        <div class="email-body">
            <div class="greeting">Hi Team,</div>
            
            <div class="content">
                {content[0]}
            </div>
            
             <div class="batch-report-section" style="display: flex; gap: 20px;column-gap: 10px; margin-bottom: 20px;">
                <div style="background-color: #f0f0f0; border-radius: 5px; overflow: hidden; display: flex;">
                    <div style="padding: 10px; background-color: #e0e0e0; font-weight: bold;">Batch ID:</div>
                    <div style="padding: 10px;">{ETLBatchId}</div>
                </div>
                <div style="background-color: #f0f0f0; border-radius: 5px; overflow: hidden; display: flex;">
                    <div style="padding: 10px; background-color: #e0e0e0; font-weight: bold;">Report Date:</div>
                    <div style="padding: 10px;">2025-05-15</div>
                </div>
            </div>

            
            {message}
            
            <div class="content">
                {content[1]}
            </div>
            
            
            <div class="divider"></div>
            
            <div class="content" style="font-style: italic; color: #ba1d1d;">
                This is a system-generated email. Please do not reply to this message.
            </div>
            
            <div class="signature">
                <div class="name">Regards,</div>
                <div class="name">Vishwanath K</div>
                <div class="name">Microsoft Fabric Data Engineer</div>
            </div>
        </div>
        
        <div class="email-footer">
            <div>
            <img style= 'border-radius: 25px'src="https://miro.medium.com/v2/resize:fit:1000/1*7DUq1lvkZnByiqOHjLd_Zw.png" alt="fabric-logo" class="fabric-logo">
        </div>
        </div>
    </div>
</body>
</html>
 """


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import json

val = {
    "email_body": email_body,
    "recipient_email": recipient_email,
    "subject": subject
}
json_str = json.dumps(val)
mssparkutils.notebook.exit(json_str)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
