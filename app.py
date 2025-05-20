import streamlit as st
import pandas as pd
from utils.data_processor import process_excel, get_l2_user_inputs, generate_download_files, check_nominal, get_l2_descriptions

st.set_page_config(layout="wide")
st.title("🧾 Staff Incentive Management System")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        if check_nominal(uploaded_file):
            st.success("Data with Nominal 505XXXXXXX is loaded.")
            l2_values = get_l2_descriptions(uploaded_file)

            user_inputs = get_l2_user_inputs(l2_values)

            if st.button("Generate Output Files"):
                raw_df, staff_incentive_df, pivots, l2_outputs = generate_download_files(
                    uploaded_file, user_inputs
                )

                st.download_button("📥 Download Raw Pivot", pivots["raw"], file_name="Raw_Pivot.xlsx")
                st.download_button("📥 Download Staff Incentive Raw Data", staff_incentive_df.to_excel(index=False), file_name="Staff_Incentive_Raw_Data.xlsx")
                st.download_button("📥 Download Staff Incentive Pivot", pivots["incentive"], file_name="Staff_Incentive_Pivot.xlsx")

                st.subheader("📂 Download Individual L2 Files")
                for l2, file in l2_outputs.items():
                    st.download_button(f"📁 {l2}", file, file_name=f"{l2}.xlsx")

    except Exception as e:
        st.error(f"Processing failed: {e}")
