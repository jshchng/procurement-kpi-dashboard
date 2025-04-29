# main.py

from src.data_cleaning import load_data, clean_data
from src.feature_engineering import engineer_features
from src.analysis import supplier_performance_summary, find_top_suppliers
from src.visualization import plot_delivery_delays, plot_defect_rate, plot_compliance

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

    # 4. Analysis
    summary = supplier_performance_summary(df)
    summary.to_csv("outputs/supplier_performance_summary.csv")
    print("Supplier performance summary saved at outputs/supplier_performance_summary.csv")

    # 5. Visualization
    plot_delivery_delays(df, save_path="outputs/plots/delivery_delay_distribution.png")
    plot_defect_rate(df, save_path="outputs/plots/defect_rate_by_supplier.png")
    plot_compliance(df, save_path="outputs/plots/compliance_distribution.png")

if __name__ == "__main__":
    main()
