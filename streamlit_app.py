import streamlit as st
import pandas as pd
import io
import os

def read_csv_file(file):
    try:
        # Try different encodings and delimiters
        encodings = ['utf-8', 'latin-1', 'iso-8859-1']
        delimiters = [',', ';', '\t', '|']
        
        for encoding in encodings:
            for delimiter in delimiters:
                try:
                    df = pd.read_csv(file, encoding=encoding, sep=delimiter)
                    if not df.empty and len(df.columns) > 1:
                        return df, None
                except:
                    pass
        
        return None, "Unable to read the file. Please check the file format and encoding."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

def merge_csv_files(files, identifier):
    dataframes = []
    for file in files:
        df, error = read_csv_file(file)
        if df is not None:
            dataframes.append(df)
        else:
            st.error(f"Error in file {file.name}: {error}")
    
    if not dataframes:
        return None, "No valid CSV files were found."
    
    # Find common columns across all dataframes
    common_columns = set.intersection(*[set(df.columns) for df in dataframes])
    
    if identifier not in common_columns:
        return None, f"The selected identifier '{identifier}' is not present in all files."
    
    # Keep only common columns and merge
    dataframes = [df[list(common_columns)] for df in dataframes]
    merged_df = pd.concat(dataframes, ignore_index=True)
    
    # Remove duplicates based on the identifier
    merged_df.drop_duplicates(subset=[identifier], keep='first', inplace=True)
    
    return merged_df, None

st.title("CSV File Merger")

uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=True, type="csv")

if uploaded_files:
    st.write(f"Number of files uploaded: {len(uploaded_files)}")
    
    # Read the first file to get potential identifiers
    first_df, error = read_csv_file(uploaded_files[0])
    if first_df is not None:
        potential_identifiers = first_df.columns.tolist()
        unique_identifier = st.selectbox("Select the unique identifier column", potential_identifiers)
        
        if st.button("Merge Files"):
            merged_df, error = merge_csv_files(uploaded_files, unique_identifier)
            
            if merged_df is not None:
                st.success("Files merged successfully!")
                st.write(f"Total rows in merged file: {len(merged_df)}")
                st.write(f"Columns in merged file: {', '.join(merged_df.columns)}")
                
                st.dataframe(merged_df.head())
                
                csv_buffer = io.StringIO()
                merged_df.to_csv(csv_buffer, index=False)
                csv_str = csv_buffer.getvalue()
                
                st.download_button(
                    label="Download Merged CSV",
                    data=csv_str,
                    file_name="merged_file.csv",
                    mime="text/csv"
                )
            else:
                st.error(f"Merging failed: {error}")
    else:
        st.error(f"Error reading the first file: {error}")
else:
    st.info("Please upload CSV files to merge.")

# Display file details
if uploaded_files:
    st.subheader("Uploaded File Details:")
    for file in uploaded_files:
        df, error = read_csv_file(file)
        if df is not None:
            st.write(f"File: {file.name}")
            st.write(f"Columns: {', '.join(df.columns)}")
            st.write(f"Rows: {len(df)}")
            st.write("---")
        else:
            st.error(f"Error in file {file.name}: {error}")
