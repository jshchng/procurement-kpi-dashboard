# src/visualization.py

import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_delivery_delays(df, save_path=None):
    plt.figure(figsize=(8,5))
    sns.histplot(df['Delivery_Delay_Days'].dropna(), bins=20, kde=True, color="skyblue")
    plt.title("Delivery Delay Distribution")
    plt.xlabel("Delivery Delay (days)")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_defect_rate(df, save_path=None):
    plt.figure(figsize=(12,6))
    supplier_defects = df.groupby('Supplier')['Defect_Rate'].mean().sort_values()
    supplier_defects.plot(kind='bar', color='salmon')
    plt.title('Average Defect Rate per Supplier')
    plt.ylabel('Defect Rate')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_compliance(df, save_path=None):
    plt.figure(figsize=(12,6))
    supplier_compliance = df.groupby('Supplier')['Compliance'].apply(lambda x: (x == 'Yes').mean()).sort_values()
    supplier_compliance.plot(kind='bar', color='lightgreen')
    plt.title('Compliance Rate per Supplier')
    plt.ylabel('Compliance Rate')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()
