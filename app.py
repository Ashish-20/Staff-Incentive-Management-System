import streamlit as st
from utils.data_processor import process_excel
import os

st.set_page_config(page_title="Staff Incentive Portal", layout="wide")
st.title("🧾 Staff Incentive Management Portal")

uploaded_file = st.file_uploader("📤 Upload Fusion Excel File", type=["xlsx"])

if uploaded_file:
    with st.spinner("Processing..."):
        result_df, summaries, l2_files = process_excel(uploaded_file)
        st.success("Data processed successfully!")

        st.subheader("📊 Summary View")
        st.dataframe(result_df)

        st.subheader("📁 Download Reports")
        for name, path in l2_files.items():
            with open(path, "rb") as f:
                st.download_button(f"Download {name}", f, file_name=os.path.basename(path))

        st.info("📧 Email functionality is available only in the desktop version.")