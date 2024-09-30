import streamlit as st
import pandas as pd
import io

def check_csv_file(file):
    try:
        df = pd.read_csv(file)
        if df.empty:
            return False, "The file is empty."
        if len(df.columns) == 0:
            return False, "The file has no columns."
        return True, df
    except pd.errors.EmptyDataError:
        return False, "The file is empty or contains no data."
    except pd.errors.ParserError:
        return False, "Unable to parse the file. Please check if it's a valid CSV."
    except Exception as e:
        return False, f"An error occurred while reading the file: {str(e)}"

def merge_csv_files(files, identifier):
    dataframes = []
    for file in files:
        success, result = check_csv_file(file)
        if not success:
            st.error(f"Error in file {file.name}: {result}")
            return None
        dataframes.append(result)
    
    if not dataframes:
        st.error("No valid CSV files were uploaded.")
        return None
    
    merged_df = pd.concat(dataframes, ignore_index=True).drop_duplicates(subset=[identifier])
    return merged_df

st.title("CSV File Merger")

uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=True, type="csv")

if uploaded_files:
    # Check the first file to get column names
    success, result = check_csv_file(uploaded_files[0])
    if success:
        sample_df = result
        unique_identifier = st.selectbox("Select the unique identifier column", sample_df.columns)

        if st.button("Merge Files"):
            merged_df = merge_csv_files(uploaded_files, unique_identifier)
            if merged_df is not None:
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
                st.dataframe(merged_df.head())
    else:
        st.error(f"Error in the first uploaded file: {result}")
else:
    st.info("Please upload CSV files to merge.")
