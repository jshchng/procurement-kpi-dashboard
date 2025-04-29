# src/feature_engineering.py

import pandas as pd

def engineer_features(df):
    """Create delivery delay, discount percent, defect rate, total spend."""
    df['Delivery_Delay_Days'] = (df['Delivery_Date'] - df['Order_Date']).dt.days
    df['Discount_Percent'] = (df['Unit_Price'] - df['Negotiated_Price']) / df['Unit_Price'] * 100
    df['Defect_Rate'] = df['Defective_Units'] / df['Quantity']
    df['Total_Spend'] = df['Quantity'] * df['Negotiated_Price']
    
    return df
