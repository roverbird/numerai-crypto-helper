# A script to automate crypto signals submission to https://crypto.numer.ai/submissions 
# It works

import pandas as pd
from numerapi import CryptoAPI

# Initialize the CryptoAPI (for Numerai Crypto Tournament)
api = CryptoAPI(public_id="key", secret_key="key")

# Get the model name: replace 'your_model_name' with your actual model name (not the uuid but the actual title of the model) 
model_id = api.get_models()['your_model_name']

# Path to your signals.csv file (file must contain headers: symbol,signal)
predictions_file_path = "/path/to/signals/signals.csv"
# Upload predictions for the crypto tournament

try:
    submission_id = api.upload_predictions(file_path=predictions_file_path, model_id=model_id)
    print(f"Crypto predictions uploaded successfully! Submission ID: {submission_id}")

except Exception as e:
    print(f"An error occurred while uploading predictions: {e}")
