import streamlit as st
import pandas as pd
import os
import io

def load_csv(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error(f"Error reading file {file.name}: {str(e)}")
        return None

def comprehensive_merge(dfs, unique_identifier):
    # Start with the first DataFrame to maintain its order
    merged_df = dfs[0]
    
    # Create a set of existing identifiers
    existing_ids = set(merged_df[unique_identifier])
    
    # Iterate through the rest of the DataFrames
    for df in dfs[1:]:
        # Ensure the unique identifier is in the current DataFrame
        if unique_identifier not in df.columns:
            st.warning(f"Unique identifier '{unique_identifier}' not found in one of the files. Skipping this file.")
            continue
        
        # Identify new columns in the current DataFrame
        new_columns = [col for col in df.columns if col not in merged_df.columns and col != unique_identifier]
        
        # Identify new rows in the current DataFrame
        new_rows = df[~df[unique_identifier].isin(existing_ids)]
        
        # Add new columns to merged_df (fill with NaN for existing rows)
        for col in new_columns:
            merged_df[col] = pd.NA
        
        # Update existing rows with new data
        merged_df.update(df.set_index(unique_identifier), overwrite=False)
        
        # Append new rows
        merged_df = pd.concat([merged_df, new_rows[merged_df.columns]], ignore_index=True)
        
        # Update the set of existing identifiers
        existing_ids.update(new_rows[unique_identifier])
    
    return merged_df

def merge_csvs(files, unique_identifier):
    dfs = []
    for file in files:
        df = load_csv(file)
        if df is not None:
            # Ensure the unique identifier is in the DataFrame
            if unique_identifier not in df.columns:
                st.warning(f"Unique identifier '{unique_identifier}' not found in file {file.name}. Skipping this file.")
                continue
            dfs.append(df)
    
    if not dfs:
        st.error("No valid CSV files were uploaded or all files were skipped due to missing identifier.")
        return None
    
    try:
        merged_df = comprehensive_merge(dfs, unique_identifier)
    except Exception as e:
        st.error(f"Error merging files: {str(e)}")
        return None
    
    return merged_df

def main():
    st.set_page_config(page_title="CSV Merger App", layout="wide")
    
    st.title("CSV Merger App")
    st.write("This app merges multiple CSV files into a master CSV file using a unique identifier, combining all unique data and columns while maintaining the original order.")
    
    # File uploader
    uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=True, type="csv")
    
    if uploaded_files:
        st.write("Uploaded files:")
        for file in uploaded_files:
            st.write(f"- {file.name}")
        
        # Unique identifier input
        unique_identifier = st.text_input("Enter the unique identifier column name:")
        
        if st.button("Merge CSV Files"):
            if not unique_identifier:
                st.error("Please enter a unique identifier column name.")
            else:
                with st.spinner("Merging CSV files..."):
                    merged_df = merge_csvs(uploaded_files, unique_identifier)
                    
                if merged_df is not None:
                    st.success("CSV files merged successfully!")
                    
                    # Display merged DataFrame
                    st.subheader("Merged Data Preview")
                    st.dataframe(merged_df.head())
                    
                    # Download button for merged CSV
                    csv = merged_df.to_csv(index=False)
                    st.download_button(
                        label="Download Merged CSV",
                        data=csv,
                        file_name="merged_data.csv",
                        mime="text/csv",
                    )
                    
                    # Display statistics
                    st.subheader("Merged Data Statistics")
                    st.write(f"Total rows: {len(merged_df)}")
                    st.write(f"Total columns: {len(merged_df.columns)}")
                    
                    # Display column names
                    st.subheader("Columns in Merged Data")
                    st.write(", ".join(merged_df.columns))

if __name__ == "__main__":
    main()
