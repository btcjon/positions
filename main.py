import requests
import pandas as pd
import io
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apitable import Apitable
import numpy as np

# Set up logging
logging.basicConfig(filename='update_log.log', level=logging.INFO, format='%(asctime)s %(message)s')

csv_url = 'https://www.fxblue.com/users/compoundit/csv'
access_token = 'uskr7IEUFGLArGCDjxjBmPH'
datasheet_id = 'dstTbH8nkfwx8qsfV0'

logging.info("Starting the update process.")

# Function to fetch and process CSV data
def fetch_and_update():
    logging.info("fetch_and_update job started.")
    try:
        logging.info("Attempting to fetch CSV data from the URL.")
        # Fetch and load the CSV data into a DataFrame
        response = requests.get(csv_url)
        if response.status_code != 200:
            logging.error(f"Failed to fetch CSV data. Status code: {response.status_code}")
            return
        df = pd.read_csv(io.StringIO(response.text), skiprows=1, low_memory=False)
        logging.info("CSV data fetched successfully.")

        # Preprocessing steps (placeholder values replacement, data type conversion, etc.)
        # ...

        # Initialize last_df before using it
        last_df = pd.DataFrame()
        # Load the last fetched dataset
        try:
            last_df = pd.read_csv('latest_dataset.csv')
        except FileNotFoundError:
            logging.info("No previous dataset found. Starting fresh.")

        # Check if 'Type' column exists
        if 'Type' not in df.columns:
            logging.error("'Type' column is missing from the fetched CSV data.")
            return

        # Identify new and updated "Open position" records
        logging.info("Identifying new and updated 'Open position' records.")
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

        # Apply the function to each record in records_payload
        records_payload_sanitized = [replace_invalid_json_values(record) for record in records_to_upload]

        # Update records in AITable
        # Note: Adjusted to match the AITable API documentation
        logging.info(f"Updating {len(records_payload_sanitized)} records in AITable.")
        response = requests.patch(
            f'https://aitable.ai/fusion/v1/datasheets/{datasheet_id}/records',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            },
            json={'records': records_payload_sanitized}
        )

        if response.status_code == 200:
            logging.info("Records updated successfully")
            logging.info(f"Response data: {response.json()}")
        else:
            logging.error(f"Failed to update records: {response.text}")
            logging.error(f"Response data: {response.json()}")

        # Store the current dataset for the next fetch
        df.to_csv('latest_dataset.csv', index=False)
        logging.info("The current dataset has been stored for the next fetch.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        logging.info("fetch_and_update job completed.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Initialize the scheduler
logging.info("Initializing the scheduler.")
scheduler = BlockingScheduler()

# Schedule the job to run every 10 minutes
logging.info("Scheduling the job to run every 10 minutes.")
scheduler.add_job(fetch_and_update, 'interval', minutes=10)

# Start the scheduler
logging.info("Starting the scheduler.")
scheduler.start()
# Provided values
access_token = 'uskr7IEUFGLArGCDjxjBmPH'
datasheet_id = 'dstTbH8nkfwx8qsfV0'
csv_url = 'https://www.fxblue.com/users/compoundit/csv'

# Initialize the Apitable client with your access token
apitable = Apitable(access_token)

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
    # Load field definitions from fields.json
    with open('fields.json', 'r') as fields_file:
        field_definitions = [json.loads(line) for line in fields_file.readlines()]

    # Create a mapping of field names to their types
    field_types = {field['name']: field['type'] for field in field_definitions}

    for key, value in record.items():
        # Check if the value matches the field type
        field_type = field_types.get(key)
        if field_type == 'Number' and isinstance(value, float):
            if np.isnan(value) or np.isinf(value):
                record[key] = None
            else:
                # Ensure the number is formatted to the correct precision
                precision = next((field['property']['precision'] for field in field_definitions if field['name'] == key and 'precision' in field['property']), None)
                if precision is not None:
                    record[key] = round(value, precision)
        elif field_type == 'DateTime' and isinstance(value, str):
            # Parse and format the date-time string to match the expected format
            format_str = next((field['property']['format'] for field in field_definitions if field['name'] == key and 'format' in field['property']), None)
            if format_str:
                try:
                    parsed_date = datetime.strptime(value, '%Y/%m/%d %H:%M:%S')
                    record[key] = parsed_date.strftime(format_str)
                except ValueError:
                    record[key] = None
        # Add additional type checks and formatting as needed based on fields.json
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