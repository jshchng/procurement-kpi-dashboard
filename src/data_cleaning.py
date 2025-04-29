# src/data_cleaning.py

import pandas as pd

def load_data(filepath):
    """Load purchase order data from CSV."""
    df = pd.read_csv(filepath)
    return df

def clean_data(df):
    """Perform basic cleaning: fix dates, fill missing values, convert types."""
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date'], errors='coerce')
    
    df['Defective_Units'] = df['Defective_Units'].fillna(0)
    
    numeric_cols = ['Quantity', 'Unit_Price', 'Negotiated_Price', 'Defective_Units']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    return df
