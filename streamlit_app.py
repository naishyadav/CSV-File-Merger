import streamlit as st
import pandas as pd
import io

def read_csv_file(file):
    try:
        df = pd.read_csv(file)
        if df.empty:
            return None, "The file is empty."
        return df, None
    except Exception as e:
        return None, f"Error reading file: {str(e)}"

def merge_csv_files(files, identifier):
    dataframes = []
    for file in files:
        df, error = read_csv_file(file)
        if df is not None:
            if identifier in df.columns:
                dataframes.append(df)
            else:
                st.warning(f"File {file.name} does not contain the identifier column '{identifier}'. Skipping this file.")
        else:
            st.warning(f"Skipping file {file.name}: {error}")
    
    if not dataframes:
        return None, "No valid dataframes to merge."

    merged_df = dataframes[0]
    for df in dataframes[1:]:
        merged_df = pd.merge(merged_df, df, on=identifier, how='outer')

    return merged_df, None

st.title("CSV File Merger")

uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=True, type="csv")

if uploaded_files:
    st.write(f"Number of files uploaded: {len(uploaded_files)}")
    
    # Read the first file to get potential identifiers
    first_df, _ = read_csv_file(uploaded_files[0])
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
        st.error("Could not read the first file to determine potential identifiers.")
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
            st.warning(f"Could not read file {file.name}: {error}")
