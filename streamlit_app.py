import streamlit as st
import pandas as pd
import io

def merge_csv_files(files, identifier):
    dataframes = []
    for file in files:
        df = pd.read_csv(file)
        dataframes.append(df)
    merged_df = pd.concat(dataframes, ignore_index=True).drop_duplicates(subset=[identifier])
    return merged_df

st.title("CSV File Merger")

uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=True, type="csv")

if uploaded_files:
    # Read the first file to get column names
    sample_df = pd.read_csv(uploaded_files[0])
    unique_identifier = st.selectbox("Select the unique identifier column", sample_df.columns)

    if st.button("Merge Files"):
        try:
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
            
            st.success("Files merged successfully!")
            st.dataframe(merged_df.head())  # Display the first few rows of the merged dataframe
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
