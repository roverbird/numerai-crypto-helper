# This script fetches current round info from Numerai API

from numerapi import CryptoAPI
from datetime import datetime, timedelta, timezone

# Initialize the CryptoAPI (for Numerai Crypto Tournament)
api = CryptoAPI(public_id="key", secret_key="key")


# Function to fetch current round information
def get_crypto_round_status():
    # GraphQL query to fetch the current round information
    query = '''
        query {
          rounds(tournament: 12) {
            number
            openTime
            closeTime
            resolveTime
          }
        }
    '''

    try:
        # Make the GraphQL query
        response = api.raw_query(query)
        rounds_info = response['data']['rounds']

        # Find the latest round (assuming the last one in the list is the current one)
        if rounds_info:
            current_round = rounds_info[0]  # Select the first round (most recent)

            # Convert openTime, closeTime, and resolveTime to datetime objects using fromisoformat
            open_time = datetime.fromisoformat(current_round['openTime'].replace("Z", "+00:00"))
            close_time = datetime.fromisoformat(current_round['closeTime'].replace("Z", "+00:00"))
            resolve_time = datetime.fromisoformat(current_round['resolveTime'].replace("Z", "+00:00"))

            # Print current round info
            print(f"Round Number: {current_round['number']}")
            print(f"Open Time: {open_time}")
            print(f"Close Time: {close_time}")
            print(f"Resolve Time: {resolve_time}")

            # Get current UTC time and make it offset-aware
            current_time = datetime.utcnow().replace(tzinfo=timezone.utc)

            # Check if the round opened within the last 12 hours
            time_difference = current_time - open_time
            if time_difference <= timedelta(hours=12):
                print("New round has started within the last 12 hours!")
            else:
                print("No new round within the last 12 hours.")

        else:
            print("No current round found.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to fetch round information
get_crypto_round_status()

