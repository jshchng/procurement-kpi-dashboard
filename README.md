# Procurement KPI Dashboard

An interactive Streamlit dashboard for analyzing procurement performance across key indicators such as:

- Delivery delays
- Defect rates
- Compliance rates

## 📊 Features

- Filter by supplier and order date range
- Visualize supplier delivery performance
- Analyze quality and compliance trends
- Designed for supply chain and operations analytics roles

## 📁 Data

This dashboard uses a synthetic dataset of anonymized purchase orders from 2022–2023. Data is cleaned and enhanced with feature engineering:

- `Delivery_Delay_Days`
- `Defect_Rate`
- `Compliance` (binary mapping)

## 🚀 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/jshchng/procurement-kpi-dashboard.git
   cd procurement-kpi-dashboard

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Launch dashboard:
   ```bash
   streamlit run src/dashboard.py
