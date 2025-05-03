# src/dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.analysis import supplier_performance_summary
from src.data_cleaning import clean_data
from src.feature_engineering import engineer_features

# Function to load the data (used for session state)
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

def main():
    st.title("Procurement KPI Analysis Dashboard")
    st.markdown("### A modern dashboard to explore procurement data interactively")

    # Load data if it's not in session state
    if 'df' not in st.session_state:
        file_path = 'data/procurement_kpi_cleaned.csv'
        df = load_data(file_path)
        df = clean_data(df)
        df = engineer_features(df)
        st.session_state.df = df

    df = st.session_state.df

    # Sidebar filters
    st.sidebar.title("Filters")
    suppliers = df['Supplier'].dropna().unique()
    selected_suppliers = st.sidebar.multiselect("Select Supplier", suppliers, default=suppliers)
    categories = df['Item_Category'].dropna().unique()
    selected_categories = st.sidebar.multiselect("Select Item Category", categories, default=categories)

    filtered_df = df[
        df['Supplier'].isin(selected_suppliers) & df['Item_Category'].isin(selected_categories)
    ]

    # Ensure dates are valid before filtering
    filtered_df = filtered_df.dropna(subset=['Order_Date'])

    st.sidebar.subheader("Select Date Range")
    if not filtered_df.empty and pd.notnull(filtered_df['Order_Date'].min()):
        min_date = filtered_df['Order_Date'].min().date()
        max_date = filtered_df['Order_Date'].max().date()
    else:
        min_date = pd.to_datetime("2022-01-01").date()
        max_date = pd.to_datetime("2024-01-01").date()

    # Date range selector
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date]
    )

    # Ensure we have a list or tuple with 2 dates
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    elif isinstance(date_range, pd.Timestamp):
        start_date = end_date = date_range
    else:
        # Allow Streamlit to default to full data range instead of stopping
        st.warning("Invalid date selection. Showing full dataset.")
        start_date = df['Order_Date'].min()
        end_date = df['Order_Date'].max()

    # Filter by selected date range
    filtered_df = filtered_df[
        (filtered_df['Order_Date'] >= pd.to_datetime(start_date)) &
        (filtered_df['Order_Date'] <= pd.to_datetime(end_date))
    ]

    # KPI Metrics
    st.subheader("📊 Key Metrics")
    total_spend = (filtered_df['Quantity'] * filtered_df['Negotiated_Price']).sum()
    total_savings = ((filtered_df['Quantity'] * (filtered_df['Unit_Price'] - filtered_df['Negotiated_Price'])).sum())
    avg_delivery_delay = filtered_df['Delivery_Delay_Days'].mean()
    defect_rate = (filtered_df['Defective_Units'].sum() / filtered_df['Quantity'].sum()) if filtered_df['Quantity'].sum() > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Spend", f"${total_spend:,.0f}")
    col2.metric("Cost Savings", f"${total_savings:,.0f}")
    col3.metric("Avg Delivery Delay", f"{avg_delivery_delay:.1f} days")
    col4.metric("Defect Rate", f"{defect_rate:.2%}")

    # Filtered Data Preview
    st.header("Filtered Data Preview")
    st.dataframe(filtered_df.head())

    # KPI Summary
    summary = supplier_performance_summary(filtered_df)
    st.header("Supplier Performance Summary")
    st.dataframe(summary)

    # Delivery delays
    st.subheader("Delivery Delay Distribution")
    fig1, ax1 = plt.subplots()
    sns.histplot(filtered_df['Delivery_Delay_Days'].dropna(), kde=True, bins=20, ax=ax1, color='skyblue')
    ax1.set_title("Delivery Delay Distribution")
    ax1.set_xlabel("Delivery Delay (days)")
    st.pyplot(fig1)

    # Defect rates
    st.subheader("Defect Rate by Supplier")
    supplier_defects = filtered_df.groupby('Supplier')['Defect_Rate'].mean().sort_values()
    if not supplier_defects.empty:
        fig2, ax2 = plt.subplots()
        supplier_defects.plot(kind='bar', ax=ax2, color='salmon', edgecolor='black', linewidth=1)
        ax2.set_title('Average Defect Rate per Supplier')
        ax2.set_ylabel('Defect Rate')
        st.pyplot(fig2)
    else:
        st.info("No data available for the selected filters to display defect rates.")

    # Compliance rates
    st.subheader("Compliance Rate by Supplier")
    supplier_compliance = filtered_df.groupby('Supplier')['Compliance'].apply(lambda x: (x == 'Yes').mean()).sort_values()
    if not supplier_compliance.empty and supplier_compliance.dtype.kind in 'iufc':  # numeric check
        fig3, ax3 = plt.subplots()
        supplier_compliance.plot(kind='bar', ax=ax3, color='lightgreen', edgecolor='black', linewidth=1)
        ax3.set_title('Average Compliance Rate per Supplier')
        ax3.set_ylabel('Compliance Rate')
        st.pyplot(fig3)
    else:
        st.info("No data available for the selected filters to display compliance rates.")

    # Download button
    st.sidebar.subheader("Download")
    st.sidebar.download_button("Download Filtered Data", filtered_df.to_csv(index=False), "filtered_data.csv")

if __name__ == "__main__":
    main()
