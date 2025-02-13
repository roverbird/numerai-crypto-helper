# yiedl-extractor.py
# extracts specific columns from historic yiedl dataset 
# you can use this data for numerai data contest
# works with this data: https://api.yiedl.ai/yiedl/v1/downloadDataset?type=historical
# Data is released every Monday to Friday after 12 UTC

import pandas as pd
from datetime import date

# Input Parquet file and output CSV file
PARQUET_FILE = './dataset_historical_20250201.parquet' # change to correct historical data file name
DATASET_FILE = 'yiedl_data.csv'

# Columns to keep
COLUMNS_TO_KEEP = ['date', 'symbol', 'pvm_XXXX']  # list any number of columns that you want to extract

# Start date for filtering
START_DATE = date(2023, 1, 1)  # set start date for historic data

# Function to extract columns, filter data, and save to CSV
def extract_and_save_data(parquet_file, dataset_file, columns_to_keep, start_date):
    try:
        # Load the Parquet file into a Pandas DataFrame
        df = pd.read_parquet(parquet_file, columns=columns_to_keep)
        print(f"Loaded {len(df)} rows from {parquet_file}")

        # Convert the 'date' column to datetime if it isn't already
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Filter data based on the start date
        filtered_df = df[df['date'] >= pd.to_datetime(start_date)]

        # Save the filtered DataFrame to a CSV file
        filtered_df.to_csv(dataset_file, index=False)
        print(f"Data saved to {dataset_file}")
    except Exception as e:
        print(f"Error processing file: {e}")

# Call the function
extract_and_save_data(PARQUET_FILE, DATASET_FILE, COLUMNS_TO_KEEP, START_DATE)

