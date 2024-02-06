import requests
import pandas as pd
import io
from apitable import Apitable
import numpy as np

# Provided values
access_token = 'uskr7IEUFGLArGCDjxjBmPH'
datasheet_id = 'dstTbH8nkfwx8qsfV0'
csv_url = 'https://www.fxblue.com/users/compoundit/csv'

# Initialize the Apitable client with your access token
apitable = Apitable(access_token)

# Fetch and load the CSV data into a DataFrame
response = requests.get(csv_url)
df = pd.read_csv(io.StringIO(response.text), skiprows=1, low_memory=False)

# Preprocessing steps (placeholder values replacement, data type conversion, etc.)
# ...

# Load the last fetched dataset
try:
    last_df = pd.read_csv('latest_dataset.csv')
except FileNotFoundError:
    last_df = pd.DataFrame()

# Identify new and updated "Open position" records
if not last_df.empty:
    # Merge on 'Ticket' to find differences
    merged_df = pd.merge(df, last_df, on='Ticket', how='outer', indicator=True)
    # New or updated records
    new_or_updated_records = merged_df[merged_df['_merge'] != 'right_only']
    # Filter for "Open position" or newly "Closed position"
    new_or_updated_records = new_or_updated_records[(new_or_updated_records['Type'] == 'Open position') | ((new_or_updated_records['Type'] == 'Closed position') & (merged_df['_merge'] == 'left_only'))]
else:
    new_or_updated_records = df[df['Type'] == 'Open position']

# Convert the new or updated records to a list of dictionaries for the API
records_to_upload = new_or_updated_records.to_dict(orient='records')

# Function to replace NaN, Infinity, and -Infinity in a dictionary
def replace_invalid_json_values(record):
    for key, value in record.items():
        if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
            record[key] = None
    return record

# Apply the function to each record in records_payload
records_payload_sanitized = [replace_invalid_json_values(record) for record in records_to_upload]

# Update records in AITable
# Note: Adjusted to match the AITable API documentation
response = requests.patch(
    f'https://aitable.ai/fusion/v1/datasheets/{datasheet_id}/records',
    headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    },
    json={'records': records_payload_sanitized}
)

if response.status_code == 200:
    print("Records updated successfully")
else:
    print(f"Failed to update records: {response.text}")

# Store the current dataset for the next fetch
df.to_csv('latest_dataset.csv', index=False)