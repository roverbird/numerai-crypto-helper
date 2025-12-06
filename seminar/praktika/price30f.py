# This script calculates the 30-day future returns for a given financial security by analyzing daily closing prices from a CSV file. It processes the data to get the closing price for each day, then uses vectorized operations to calculate the percentage change in price over a 30-day period. The script outputs the original date (open date), the closing price on that date, the price 30 days later (close date), and the 30-day future return percentage, saving the results to a new CSV file.
#
# Input file requirements: input csv must contain hourly data, timestamp, symbol (ticker), price (real price at the date and time in timestamp)
#
# Usage: python3 02price30f.py <real_price_input_data.csv> <output_30_days_roll.csv>

import pandas as pd
import sys

# Get input and output file names from command line arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# Read the CSV input file with no headers
data = pd.read_csv(input_file, header=None, names=['timestamp', 'symbol', 'price'])

# Convert the 'timestamp' column to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Extract the symbol from the first row (since the input file contains only one symbol)
symbol = data['symbol'].iloc[0]

# Create a new column for the date
data['date'] = data['timestamp'].dt.date

# Exclude 00:00:00 timestamps and group by date to get the last (closing) price of each day
daily_close = data[data['timestamp'].dt.time != pd.to_datetime('00:00:00').time()]  
daily_close = daily_close.groupby('date').agg({'price': 'last'}).reset_index()

# Sort by date
daily_close = daily_close.sort_values(by='date').reset_index(drop=True)

# Calculate the price 30 days into the future using shift()
daily_close['price_at_close_date'] = daily_close['price'].shift(-30)

# Calculate the close date (30 days in the future)
daily_close['close_date'] = daily_close['date'].shift(-30)

# Calculate the 30-day future return
daily_close['30_day_future_return'] = (daily_close['price_at_close_date'] - daily_close['price']) / daily_close['price'] * 100

# Drop rows where future data is not available (last 30 rows)
daily_close = daily_close.dropna(subset=['price_at_close_date', 'close_date', '30_day_future_return'])

# Add the symbol as the first column
daily_close.insert(0, 'symbol', symbol)

# Reorder the columns to match the desired output order
daily_close = daily_close[['symbol', 'date', 'price', 'close_date', 'price_at_close_date', '30_day_future_return']]

# Write the results to the output CSV file
daily_close.to_csv(output_file, index=False, header=['symbol', 'date', 'price', 'close_date', 'price_at_close_date', '30_day_future_return'])

print(f"30-day future returns calculated and saved to {output_file}")

