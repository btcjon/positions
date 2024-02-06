import requests
import pandas as pd
import io
from apitable import Apitable

# Provided values
access_token = 'uskr7IEUFGLArGCDjxjBmPH'
datasheet_id = 'dstTbH8nkfwx8qsfV0'
csv_url = 'data_sample.csv'  # Adjust this to the path of your local CSV file

# Initialize the Apitable client with your access token
apitable = Apitable(access_token)

# Fetch the CSV data
df = pd.read_csv(csv_url, skiprows=1, low_memory=False)

# Replace placeholder values with None (or an appropriate value) in the DataFrame
df.loc[df['Close time'] == '1970/01/01 00:00:00', 'Close time'] = None
df.loc[df['Close date'] == '1970/01/01', 'Close date'] = None

# Convert the 'Open price' column to string
df['Open price'] = df['Open price'].astype(str)

# Adjust column names to match AITable fields (if necessary)
# Example: Rename 'Buy/sell' to 'Buy/Sell'

# Convert date and time formats (if any adjustments are needed)

# Convert the DataFrame to a list of dictionaries for the API
records_to_upload = df.to_dict(orient='records')

# Function to split the records into chunks of 10
def chunked_iterable(iterable, size=10):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

# Split records_to_upload into chunks of 10 and bulk create records in chunks
for chunk in chunked_iterable(records_to_upload):
    datasheet = apitable.datasheet(datasheet_id)
    datasheet.records.bulk_create(chunk)