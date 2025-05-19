import pandas as pd
import os

def process_excel(file):
    df_raw = pd.read_excel(file, sheet_name="raw data")
    
    required_cols = ['Employee Name', 'Email', 'Manager', 'Claim Amount', 'L2 Description']
    df_clean = df_raw[required_cols].dropna()

    os.makedirs("output", exist_ok=True)

    l2_files = {}
    for l2_value, group in df_clean.groupby('L2 Description'):
        filename = f"output/{l2_value}.xlsx"
        group.to_excel(filename, index=False)
        l2_files[l2_value] = filename

    pivot_summary = df_clean.groupby("L2 Description")["Claim Amount"].sum().reset_index()

    return df_clean, pivot_summary, l2_files