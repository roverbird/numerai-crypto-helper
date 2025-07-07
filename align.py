# sample script to align your resolved rounds file with execution log input

import pandas as pd

file_1 = "resolved_rounds.csv"
file_2 = "execution_log.csv"

# Columns to load from file_2 only
cols_file_2 = ['date', 'model_name', 'days', 'dim', 'range']

# Load file_1 fully
df1 = pd.read_csv(file_1, on_bad_lines='skip')

# Load file_2 with selected columns only
df2 = pd.read_csv(file_2, usecols=cols_file_2)

# Normalize date columns to YYYY-MM-DD (remove time in file_2)
df1['date_key'] = pd.to_datetime(df1['date'], errors='coerce').dt.strftime('%Y-%m-%d')
df2['date_key'] = pd.to_datetime(df2['date'], errors='coerce').dt.strftime('%Y-%m-%d')

# Normalize model_name as string (strip whitespace)
df1['model_name'] = df1['model_name'].astype(str).str.strip()
df2['model_name'] = df2['model_name'].astype(str).str.strip()

# Merge on date_key and model_name
merged_df = pd.merge(df1, df2, on=['model_name', 'date_key'], how='inner')

# Sort and save
merged_df = merged_df.sort_values(by=['model_name', 'date_key'])
merged_df.to_csv("aligned_output.csv", index=False)

print(f"Merged file saved as 'aligned_output.csv' with {len(merged_df)} rows.")

