The CSV Merger App is a Streamlit-based web application that allows users to merge multiple CSV files into a single master file. It uses a unique identifier to combine data across files, preserving the original order of the first file while incorporating new data from subsequent files.

**Features**

- Merge multiple CSV files into a single master file
- Use a unique identifier to match and combine data across files
- Preserve the order of rows from the first CSV file
- Add new rows from subsequent files
- Handle missing columns gracefully
- Provide detailed statistics about the merged data
- Offer a user-friendly web interface using Streamlit


**How It Works**

The app loads each uploaded CSV file into a pandas DataFrame.
It checks for the presence of the specified unique identifier in each file.
The merge process starts with the first file and sequentially incorporates data from subsequent files.
New columns are added as they appear in subsequent files.
Existing rows are updated with new data, and new rows are appended.
The final merged DataFrame is presented for preview and download.

**Limitations**

All CSV files must contain the specified unique identifier column.
The app assumes that the first uploaded file contains the desired row order.
Large files may take longer to process depending on your system's capabilities.
