import os
import requests
import zipfile
import pandas as pd

# Configuration
download_url = "https://api.yiedl.ai/yiedl/v1/downloadDataset?type=weekly"
input_file = "dataset/train_dataset.csv"
input_file_validation = "dataset/validation_dataset.csv"
output_dir = "extracted_files"
columns_to_extract = ['date', 'symbol', 'target_neutral', 'target_updown']  # set columns that you need to extract
filtered_output_file = "output.csv"
processed_dir = "processed"
size = 170 # set min numeber of observations allowed for each symbol

# Ensure necessary directories exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)

# Download the archive
archive_path = os.path.join(output_dir, "archive.zip")
print(f"Downloading archive from {download_url}...")
response = requests.get(download_url)
response.raise_for_status()
with open(archive_path, "wb") as f:
    f.write(response.content)
print(f"Archive downloaded to {archive_path}")

# Extract specific files from the archive
print(f"Extracting {input_file} and {input_file_validation}...")
with zipfile.ZipFile(archive_path, 'r') as zip_ref:
    if input_file not in zip_ref.namelist() or input_file_validation not in zip_ref.namelist():
        raise FileNotFoundError("One or more required files not found in the archive.")
    zip_ref.extract(input_file, output_dir)
    zip_ref.extract(input_file_validation, output_dir)

extracted_file_path = os.path.join(output_dir, input_file)
extracted_validation_path = os.path.join(output_dir, input_file_validation)

# Remove the downloaded archive
os.remove(archive_path)
print(f"Removed archive {archive_path}")

# Extract unique symbols from the validation file
print(f"Extracting unique symbols from {input_file_validation}...")
validation_symbols = set()
with pd.read_csv(extracted_validation_path, usecols=['symbol'], chunksize=10000) as reader:
    for chunk in reader:
        validation_symbols.update(chunk['symbol'].dropna().unique())

print(f"Found {len(validation_symbols)} unique symbols in {input_file_validation}")

# Process the main CSV file in chunks and filter by validation symbols
print(f"Filtering {input_file} based on symbols from {input_file_validation}...")
with pd.read_csv(extracted_file_path, usecols=columns_to_extract, chunksize=10000) as reader:
    for i, chunk in enumerate(reader):
        filtered_chunk = chunk[chunk['symbol'].isin(validation_symbols)]
        filtered_chunk.to_csv(filtered_output_file, mode='w' if i == 0 else 'a', index=False, header=(i == 0))

print(f"Filtered data saved to {filtered_output_file}")

# Remove extracted files and directory if empty
for file_path in [extracted_file_path, extracted_validation_path]:
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed extracted file {file_path}")
if not os.listdir(output_dir):
    os.rmdir(output_dir)
    print(f"Removed empty directory {output_dir}")

# Processing the filtered data
data = pd.read_csv(filtered_output_file)

# Ensure the required columns are present
required_columns = {"date", "symbol", "target_neutral", "target_updown"}
if not required_columns.issubset(data.columns):
    raise ValueError(f"Input file must contain the following columns: {', '.join(required_columns)}")

# Group by 'symbol' and save each group if size > threshold
for symbol, group in data.groupby("symbol"):
    if len(group) > size:
        output_file = os.path.join(processed_dir, f"{symbol}_proc.csv")
        group.to_csv(output_file, index=False)
        print(f"Processed and saved: {output_file}")

print("All files processed successfully.")

