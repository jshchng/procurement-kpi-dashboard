# src/analysis.py

import pandas as pd

def supplier_performance_summary(df):
    """Summarize supplier KPIs."""
    summary = df.groupby('Supplier').agg({
        'Defect_Rate': 'mean',
        'Delivery_Delay_Days': 'mean',
        'Discount_Percent': 'mean',
        'Total_Spend': 'sum',
        'Compliance': lambda x: (x == 'Yes').mean()
    }).rename(columns={'Compliance': 'Compliance_Rate'}).sort_values(by='Compliance_Rate', ascending=False)
    
    return summary

def find_top_suppliers(summary_df, defect_threshold=0.02, compliance_threshold=0.95):
    """Find top suppliers based on defect rate and compliance rate."""
    top_suppliers = summary_df[(summary_df['Defect_Rate'] < defect_threshold) & (summary_df['Compliance_Rate'] > compliance_threshold)]
    return top_suppliers
