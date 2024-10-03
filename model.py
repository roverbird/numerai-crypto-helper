# This script fetches info about the model by its title
# Usage: python get_model_facts.py <model_id>
# <model_id> is the human-readable name of the model

from numerapi import CryptoAPI
import sys

# Function to initialize the CryptoAPI (for Numerai Crypto Tournament)
def initialize_api():
    return CryptoAPI(public_id="key", secret_key="key")


def get_model_facts(model_id: str):
    api = initialize_api()  # Create a new session for each request

    # Updated GraphQL query with correct field names
    query = '''
    query($modelId: String!) {
      model(modelId: $modelId) {
        id
        name
        latestSubmission {
          id
          insertedAt
        }
        signalsStake {
          stakeValue
        }
        v2Stake {
          stakeValue
          pendingV2ChangeStakeRequest {
            requestedAmount
          }
        }
      }
    }
    '''

    try:
        # Fetch all models to find the UUID for the provided model name
        models = api.get_models()
        print("Authentication successful. Models:", models)

        # If the model_id is a name (not a UUID), fetch the corresponding UUID
        if model_id in models:
            model_id = models[model_id]  # Use the UUID associated with the model name
        else:
            print(f"Model name '{model_id}' not found.")
            return

    except Exception as e:
        print(f"Authentication failed: {e}")
        return  # Stop further execution if authentication fails
        
    variables = {'modelId': model_id}
    
    try:
        # Fetch model details using the GraphQL query
        response = api.raw_query(query, variables, authorization=True)
        model_info = response['data']['model']
        
        # Extract and print key details about the model
        print(f"Model ID: {model_info['id']}")
        print(f"Model Name: {model_info['name']}")
        
        # Latest submission info
        if model_info['latestSubmission']:
            latest_submission = model_info['latestSubmission']
            print(f"Latest Submission ID: {latest_submission['id']}")
            print(f"Submission Time: {latest_submission['insertedAt']}")
        else:
            print("No recent submission found.")
        
        # Signals stake
        if model_info['signalsStake']:
            print(f"Signals Staked NMR: {model_info['signalsStake']['stakeValue']}")

        # v2 Stake info
        if model_info['v2Stake']:
            print(f"V2 Staked Amount: {model_info['v2Stake']['stakeValue']}")
            
            if model_info['v2Stake']['pendingV2ChangeStakeRequest']:
                pending_request = model_info['v2Stake']['pendingV2ChangeStakeRequest']
                print(f"Pending V2 Stake Change Request Amount: {pending_request['requestedAmount']}")
            else:
                print("No pending stake change requests.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Main function to run the utility with a provided model ID
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_model_facts.py <model_id>")
        sys.exit(1)

    model_id = sys.argv[1]
    get_model_facts(model_id)
