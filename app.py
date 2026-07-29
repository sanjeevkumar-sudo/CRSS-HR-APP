"""
CRSS HR Automated Reporting Portal
"""

import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="CRSS HR Reporting Hub", layout="wide")
st.title("📊 CRSS HR Automated Reporting System")

# Sidebar Data Input
st.sidebar.header("Data Control Center")
uploaded_file = st.sidebar.file_uploader("Upload Daily HR Raw Data (.csv, .xlsx, .xls)", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    # Fail-safe file reader for CSV and Excel formats
    file_name = uploaded_file.name.lower()
    try:
        if file_name.endswith('.csv'):
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='latin1')
        else:
            df = pd.read_excel(uploaded_file)
            
        st.sidebar.success("File uploaded successfully!")
        
        # Global Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", len(df))
        col2.metric("Total Columns", len(df.columns))
        col3.metric("Data Status", "Ready")

        # Main Tabs
        tab1, tab2 = st.tabs(["📁 Standard Preset Reports", "🤖 Custom AI Report Studio"])

        with tab1:
            st.subheader("Department Report Generator")
            
            # Smart column selection
            dept_col = None
            for col in df.columns:
                if col.strip().lower() in ['department', 'dept', 'dept_name', 'dep']:
                    dept_col = col
                    break

            if dept_col:
                departments = ["All"] + list(df[dept_col].dropna().unique())
                selected_dept = st.selectbox("Select Department", departments)
            else:
                selected_dept = "All"
                st.info("Note: 'Department' column not detected automatically. Displaying full dataset.")

            frequency = st.radio("Frequency", ["Daily", "Weekly", "Monthly"], horizontal=True)
            
            if st.button("Generate Report"):
                if dept_col and selected_dept != "All":
                    filtered_df = df[df[dept_col] == selected_dept]
                else:
                    filtered_df = df

                st.write(f"### Preview for {selected_dept} ({frequency}):")
                st.dataframe(filtered_df, use_container_width=True)

                # Excel Download Button
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    filtered_df.to_excel(writer, index=False, sheet_name='HR_Report')
                
                st.download_button(
                    label="📥 Download Excel File",
                    data=buffer.getvalue(),
                    file_name=f"{selected_dept}_{frequency}_Report.xlsx",
                    mime="application/vnd.ms-excel"
                )

        with tab2:
            st.subheader("Natural Language Custom Report")
            user_query = st.text_input("Ask a question about your HR data:")
            if user_query:
                st.write(f"Query received: *'{user_query}'*")
                st.dataframe(df.head(10), use_container_width=True)

    except Exception as e:
        st.error(f"Error reading file: {e}. Please ensure the file is a valid Excel or CSV spreadsheet.")

else:
    st.info("👈 Please upload your daily Excel or CSV file in the sidebar to begin.")
