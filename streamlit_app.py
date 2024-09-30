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
    # Start with the first DataFrame
    merged_df = dfs[0]
    
    # Iterate through the rest of the DataFrames
    for df in dfs[1:]:
        # Identify new columns in the current DataFrame
        new_columns = [col for col in df.columns if col not in merged_df.columns and col != unique_identifier]
        
        # Merge the current DataFrame with only its new columns
        merged_df = pd.merge(
            merged_df, 
            df[[unique_identifier] + new_columns], 
            on=unique_identifier, 
            how='outer'
        )
    
    return merged_df

def merge_csvs(files, unique_identifier):
    dfs = []
    for file in files:
        df = load_csv(file)
        if df is not None:
            dfs.append(df)
        else:
            return None
    
    if not dfs:
        st.error("No valid CSV files were uploaded.")
        return None
    
    # Check if the unique identifier exists in all DataFrames
    for i, df in enumerate(dfs):
        if unique_identifier not in df.columns:
            st.error(f"Error: The unique identifier '{unique_identifier}' is not present in file {files[i].name}.")
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
    st.write("This app merges multiple CSV files into a master CSV file using a unique identifier, combining all unique data and columns.")
    
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
