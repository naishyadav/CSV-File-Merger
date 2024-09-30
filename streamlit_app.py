import streamlit as st
import pandas as pd
import io

st.title("CSV File Merger")

## File Upload Section
uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=True, type="csv")

## Unique Identifier Selection
if uploaded_files:
    sample_df = pd.read_csv(uploaded_files[0])
    unique_identifier = st.selectbox("Select the unique identifier column", sample_df.columns)

    if st.button("Merge Files"):
        # Merge logic here
        merged_df = merge_csv_files(uploaded_files, unique_identifier)
        
        # Create a download button for the merged file
        csv_buffer = io.StringIO()
        merged_df.to_csv(csv_buffer, index=False)
        csv_str = csv_buffer.getvalue()
        
        st.download_button(
            label="Download Merged CSV",
            data=csv_str,
            file_name="merged_file.csv",
            mime="text/csv"
        )

def merge_csv_files(files, identifier):
    dataframes = [pd.read_csv(file) for file in files]
    merged_df = pd.concat(dataframes, ignore_index=True).drop_duplicates(subset=[identifier])
    return merged_df
