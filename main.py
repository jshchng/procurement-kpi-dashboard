# main.py

from src.data_cleaning import load_data, clean_data
from src.feature_engineering import engineer_features

def main():
    # 1. Load and Clean Data
    data_path = "data/procurement_data.csv"
    df = load_data(data_path)
    df = clean_data(df)

    # 2. Feature Engineering
    df = engineer_features(df)

    # 3. Save cleaned data
    df.to_csv("data/procurement_kpi_cleaned.csv", index=False)
    print("Cleaned data saved at data/procurement_kpi_cleaned.csv")

if __name__ == "__main__":
    main()
