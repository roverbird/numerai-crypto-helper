# Numerai Crypto Helper

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

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/numerai-crypto-helper.git
   cd numerai-crypto-helper
   ```

2. Install the required dependencies:
   ```bash
   pip install numerapi
   ```

3. Run any of the scripts as needed:
   ```bash
   python round.py
   python model.py <model_title>
   python submit.py
   python submitCLI.py <model_name> <path_to_signals_csv>
   ```

## Disclaimer

This repository is not officially affiliated with Numerai. No liability of any kind. Use and modify these utilities at your own risk, and always refer to the official [Numerai documentation](https://docs.numer.ai/) for the current authoritative information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

