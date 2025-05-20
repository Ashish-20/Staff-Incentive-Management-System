import streamlit as st
import pandas as pd
from io import BytesIO

def check_nominal(file):
    df = pd.read_excel(file, sheet_name="raw data")
    print("Columns found:", df.columns.tolist())
    return df["NOMINAL"].astype(str).str.startswith("505").any()

def get_l2_descriptions(file):
    df = pd.read_excel(file, sheet_name="raw data")
    return df["L2 Description"].dropna().unique()

def get_l2_user_inputs(l2_values):
    inputs = {}
    for l2 in l2_values:
        st.subheader(f"L2 Description: {l2}")
        headcount = st.number_input(f"Enter Headcount for {l2}", min_value=0, key=f"{l2}_hc")
        budget = st.number_input(f"Enter Budget (USD) for {l2}", min_value=0.0, key=f"{l2}_bdg")
        conv_rate = st.number_input(f"Enter Conversion Rate for {l2}", min_value=0.0, key=f"{l2}_rate")
        inputs[l2] = {"headcount": headcount, "budget": budget, "rate": conv_rate}
    return inputs

def generate_download_files(file, l2_inputs):
    df = pd.read_excel(file, sheet_name="raw data")

    # Raw Pivot
    raw_pivot = df.pivot_table(index="L2 Description", values="FUNCTIONAL_AMOUNT", aggfunc="sum")
    raw_buffer = BytesIO()
    raw_pivot.to_excel(raw_buffer)
    raw_buffer.seek(0)

    # Staff Incentive Data
    filtered_df = df[df["Nature of Expenses"] == "Staff Incentive"]
    columns_needed = [ "Cost Centre", "NOMINAL", "PO NO", "Budgeted USD", "Actual USD", 
    "Variance", "FY", "Period", "Country", "LOB", "Region", 
    "L2 Description", "Nature of Expenses"]
    filtered_df = filtered_df[filtered_df.columns.intersection(columns_needed)]

    # Staff Incentive Pivot
    staff_pivot = filtered_df.pivot_table(index="L2 Description", values=filtered_df.columns[-1], aggfunc="count")
    incentive_buffer = BytesIO()
    staff_pivot.to_excel(incentive_buffer)
    incentive_buffer.seek(0)

    # L2 Descriptions
    l2_outputs = {}
    for l2, data in l2_inputs.items():
        l2_df = filtered_df[filtered_df["L2 Description"] == l2]
        output_buffer = BytesIO()
        with pd.ExcelWriter(output_buffer, engine="xlsxwriter") as writer:
            l2_df.to_excel(writer, index=False, sheet_name="Data")
            # Optional: Budget vs Actuals logic here
        output_buffer.seek(0)
        l2_outputs[l2] = output_buffer

    return df, filtered_df, {"raw": raw_buffer, "incentive": incentive_buffer}, l2_outputs
