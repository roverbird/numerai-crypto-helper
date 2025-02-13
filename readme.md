# What is Yiedl data?

If you're benchmarking financial prediction models on _Numerai_, it is crucial to know about the [community data provided by YIEDL.ai](https://yiedl.ai/competition/datasets).

Numerai partnered with YIEDL to bring a comprehensive crypto dataset to Numerai Crypto. This dataset includes over ten years of cryptocurrency data, covering essential features like price volume momentum (PVM), sentiment analysis, and on-chain metrics. Just like the obfuscated data used in the classic Numerai tournament, the YIEDL dataset is encrypted to protect intellectual property while remaining highly useful for model training.

YIEDL provides two versions of its dataset:

- Historical Dataset: Contains records dating back to 2013, making it invaluable for training models using long-term crypto trends

- Latest Dataset: Covers the most recent month, optimized for quick access

While the datasets are very high-quality and usable, keep in mind that different symbols have varying time spans of coverage. Additionally, due to its massive size, managing the dataset can be challenging, requiring custom scripts for effective processing of _parquet_ and _csv_ files. Even despite the obfuscation, the datasets are a valuable asset for building robust prediction models on Numerai. My workflow is to have historic data regularly updated with the latest data files, so that in such way you only need to download the huge historic data file infrequently.

There is not much info and documentation on data science contests like _Yiedl_ or _Numerai_ , but in terms of profitability one can judge that the contests serve their purpose. For example, Numerai recently [announced](https://forum.numer.ai/t/reducing-numerai-crypto-payouts/7914), that "Numerai Crypto is far more profitable for users than our other 2 tournaments" that they host. To take part in the [Numerai crypto contest](https://crypto.numer.ai/home) one needs to get the data first. Where from? - It is really up to you: you will need to decide which data to use, how to use it, where to collect it, and so on.

Contact me if you need a consultant on machine learning operations (mlops), data collection, parsing and preparation tasks or if interested in use cases for these particular scripts. 

# What is included?

This repository contains unofficial utilities for the Numerai Crypto Signals Contest. Intended to help users interact with the Numerai API for various purposes related to the crypto signals competition only.

## Requirements

To use these utilities, you need to install the `numerapi` package:

```bash
pip install numerapi
```

## Scripts

### `round.py`

This script fetches the current round information from the Numerai API. It provides details about the ongoing round, including start and end times, and other relevant information.

### `model.py`

This script fetches information about a specific model by its title. It retrieves various details, including the model ID, latest submission information, stakes, and other relevant metrics.

### `submit.py`

This script automates the submission of crypto signals to [https://crypto.numer.ai/submissions](https://crypto.numer.ai/submissions). It streamlines the process of submitting your signals, making it easier to participate in the Numerai Crypto Tournament.

# Yiedl Extractor

`yiedl-extractor.py` is a script for extracting specific columns from the historical Yiedl dataset. This extracted data is used for the Numerai data contest.

## Features
- Loads historical dataset from a Parquet file.
- Extracts user-specified columns.
- Filters data starting from a defined date.
- Saves the filtered dataset as a CSV file.

## Usage
1. Download the historical dataset from:
   ```
https://api.yiedl.ai/yiedl/v1/downloadDataset?type=historical
   ```
   (Data is released every Monday to Friday after 12 UTC.)
2. Update `PARQUET_FILE` with the correct dataset filename.
3. Modify `COLUMNS_TO_KEEP` to specify the columns you want to extract.
4. Set `START_DATE` to filter data from the desired start date.
5. Run the script:
   ```sh
   python yiedl-extractor.py
   ```

## Configuration
- **Input Parquet File:** `dataset_historical_20250201.parquet` (Update to the latest dataset file.)
- **Output CSV File:** `yiedl_data.csv`
- **Columns to Extract:** `['date', 'symbol', 'pvm_XXXX']` (Modify as needed.)
- **Start Date:** `2023-01-01` (Adjust to filter relevant data.)

## Output
- The extracted data is saved in `yiedl_data.csv`.

## Notes
- Ensure the dataset file exists in the specified directory before running the script.
- The script automatically handles date conversion and filtering.
- Adjust the `COLUMNS_TO_KEEP` list to extract additional columns if necessary.


# Yiedl data downloader

## Overview
`yiedl-downloader.py`  downloads a dataset for the Yield Data Contest itself (not the Numerai contest). It extracts required values and processes the data based on specific symbols from a validation dataset.

## Features
- Downloads the dataset from the Yield Data Contest API.
- Extracts the necessary CSV files from the downloaded archive.
- Filters the main dataset to keep only rows with symbols found in the validation dataset.
- Saves the filtered data into an output CSV file.
- Further processes the data by grouping symbols and saving files that meet a specified size threshold.

## Prerequisites
Ensure you have the following Python libraries installed:
- `requests`
- `pandas`

## Usage
Run the script using:
```sh
python script.py
```

## Configuration
The script is pre-configured with the following settings:
- **Download URL:** `https://api.yiedl.ai/yiedl/v1/downloadDataset?type=weekly`
- **Columns Extracted:** `date`, `symbol`, `target_neutral`, `target_updown`
- **Filtered Output File:** `output.csv`
- **Minimum Rows per Symbol to Save:** `170`

## Output
- Extracted and filtered data is saved as `output.csv`.
- Processed data for each symbol meeting the row count threshold is stored in the `processed` directory.


## Notes

- The script automatically removes temporary files and directories after processing.
- Ensure you have a stable internet connection as the dataset is large.


## Disclaimer

This repository is not officially affiliated with Numerai or Yiedl. No liability of any kind. Use and modify these utilities at your own risk, and always refer to the official [Numerai documentation](https://docs.numer.ai/) for the current authoritative information.

The scripts are provided as-is without any warranty, data is used for non-commercial research purposes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

