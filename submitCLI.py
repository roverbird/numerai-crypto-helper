# A script to automate crypto signals submission to https://crypto.numer.ai/submissions 
# And extended ver that accepts command line args
# Usage: python submitCLI.py <model_name> <path_to_signals_csv>
# <model_name> use your model's human title, not uuid

import pandas as pd
from numerapi import CryptoAPI
import sys

# Initialize the CryptoAPI (for Numerai Crypto Tournament)
api = CryptoAPI(public_id="key", secret_key="key")

# Command-line arguments for model name and signals file path
if len(sys.argv) != 3:
    print("Usage: python upload.py <model_name> <path_to_signals_csv>")
    sys.exit(1)

model_name = sys.argv[1]
predictions_file_path = sys.argv[2]

# Get the model ID using the provided model name
try:
    model_id = api.get_models()[model_name]
except KeyError:
    print(f"Error: Model '{model_name}' not found.")
    sys.exit(1)

# Validate and read the signals CSV file
try:
    signals_df = pd.read_csv(predictions_file_path)
    if not {'symbol', 'signal'}.issubset(signals_df.columns):
        raise ValueError("The signals CSV must contain 'symbol' and 'signal' columns.")
except FileNotFoundError:
    print(f"Error: The file {predictions_file_path} does not exist.")
    sys.exit(1)
except ValueError as ve:
    print(ve)
    sys.exit(1)

# Upload predictions for the crypto tournament
try:
    submission_id = api.upload_predictions(file_path=predictions_file_path, model_id=model_id)
    print(f"Crypto predictions uploaded successfully! Submission ID: {submission_id}")
except Exception as e:
    print(f"An error occurred while uploading predictions: {e}")

