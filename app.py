import streamlit as st
import pandas as pd
from utils.data_processor import get_l2_user_inputs, generate_download_files, check_nominal, get_l2_descriptions
from io import BytesIO

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

                st.download_button("📥 Download Raw Data Pivot", pivots["raw"], file_name="Raw_Pivot.xlsx")
                buffer = BytesIO()
                staff_incentive_df.to_excel(buffer, index=False)
                buffer.seek(0)
                st.download_button("📥 Download Staff Incentive Raw Data", data=buffer, file_name="Staff_Incentive_Raw_Data.xlsx")
                #st.download_button("📥 Download Staff Incentive Raw Data", staff_incentive_df.to_excel(index=False), file_name="Staff_Incentive_Raw_Data.xlsx")
                st.download_button("📥 Download Staff Incentive Pivot", pivots["incentive"], file_name="Staff_Incentive_Pivot.xlsx")


                # st.subheader("📂 Download Individual L2 Files")

                # for l2, file in l2_outputs.items():
                #     col1, col2 = st.columns([3, 1])  # 3:1 ratio for download and send

                #     with col1:
                #         st.download_button(
                #             f"📥 Download {l2} File",
                #             data=file,
                #             file_name=f"{l2}_Staff_Incentive.xlsx"
                #         )

                #     with col2:
                #         if st.button(f"📧 Send Email - {l2}"):
                #             st.info("Email functionality is only available in the desktop version.")

                # st.subheader("📂 Download Individual L2 Files")

# Store email buttons for centralized handling
                send_email_flags = {}

                for l2, file in l2_outputs.items():
                    col1, col2 = st.columns(2)

                    with col1:
                        st.download_button(
                            label=f"📥 Download {l2}",
                            data=file,
                            file_name=f"{l2}_Staff_Incentive.xlsx"
                        )

                    with col2:
                    send_email_flags[l2] = st.checkbox(f"Send Email for {l2}", key=f"send_{l2}")

# One central button to simulate sending all selected emails
                if st.button("📤 Send All Selected Emails"):
                    selected = [l2 for l2, flag in send_email_flags.items() if flag]
                    if selected:
                        for l2 in selected:
                            st.success(f"Email would be sent for: {l2} (only on desktop)")
                        else:
                            st.warning("Please select at least one L2 to send email.")
             
                
                # st.subheader("📂 Download Individual L2 Files")
                # for l2, file in l2_outputs.items():
                #     st.download_button(f"📁 {l2}", file, file_name=f"{l2}.xlsx")

    except Exception as e:
        st.error(f"Processing failed: {e}")
