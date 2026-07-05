import pandas as pd
import numpy as np
from datetime import datetime

# 1. SIMULATING RAW EXCEL DATA (Dirty & Unformatted Data)
# Imagine this is an automated report exported from an ERP system that needs daily cleaning
raw_data = {
    'Transaction_ID': [101, 102, np.nan, 103, 104, 105, 106], # Contains a missing ID
    'Date': ['2026-07-01', '2026-07-01', '2026-07-02', '2026-07-02', '2026-07-03', '2026-07-03', '2026-07-03'],
    'Product_Code': ['  M8-STEEL  ', 'M8-BRASS', 'M8-STEEL', ' M10-STEEL ', 'M12-ALUM', 'M8-STEEL', 'M8-BRASS'], # Contains leading/trailing spaces
    'Quantity_Ordered': [500, -20, 300, 150, 400, np.nan, 250], # Contains a negative value and a missing value
    'Unit_Price_USD': [0.15, 0.12, 0.15, 0.25, 0.45, 0.15, 0.12]
}

df_raw = pd.DataFrame(raw_data)
print("--- RAW DATA BEFORE AUTOMATED CLEANING ---")
print(df_raw, "\n")

# =========================================================================
# 2. AUTOMATED DATA CLEANING & TRANSFORMATION PROCESS
# =========================================================================

# Step A: Drop rows where critical identifiers (like Transaction_ID) are missing
df_clean = df_raw.dropna(subset=['Transaction_ID']).copy()

# Step B: Clean up messy text data (remove accidental spaces)
df_clean['Product_Code'] = df_clean['Product_Code'].str.strip()

# Step C: Handle anomalies (Replace negative quantities or NaN with 0 or standard value)
df_clean['Quantity_Ordered'] = df_clean['Quantity_Ordered'].apply(lambda x: x if x > 0 else 0)
df_clean['Quantity_Ordered'] = df_clean['Quantity_Ordered'].fillna(0).astype(int)

# Step D: Data Transformation (Calculate Total Revenue)
df_clean['Total_Revenue_USD'] = df_clean['Quantity_Ordered'] * df_clean['Unit_Price_USD']

# =========================================================================
# 3. GENERATING EXECUTIVE SUMMARY REPORT
# =========================================================================
summary_report = df_clean.groupby('Product_Code').agg(
    Total_Units_Sold=('Quantity_Ordered', 'sum'),
    Total_Sales_USD=('Total_Revenue_USD', 'sum')
).reset_index()

print("--- CLEANED & AGGREGATED SUMMARY REPORT ---")
print(summary_report)

# =========================================================================
# 4. EXPORTING BACK TO EXCEL
# =========================================================================
# In local execution, this will automatically generate a clean, formatted Excel file
# filename = f"Cleaned_Sales_Report_{datetime.now().strftime('%Y%m%d')}.xlsx"
# summary_report.to_excel(filename, index=False)
