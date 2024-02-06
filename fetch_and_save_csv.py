import requests
import pandas as pd
import io
import logging
import time

# Set up logging
logging.basicConfig(filename='fetch_csv_log.log', level=logging.INFO, format='%(asctime)s %(message)s')

csv_url = 'https://www.fxblue.com/users/compoundit/csv'

# Function to fetch CSV data from URL and save it locally
def fetch_csv_data(csv_url):
    logging.info("Attempting to fetch CSV data from the URL.")
    try:
        response = requests.get(csv_url)
        if response.status_code == 200:
            logging.info("CSV data fetched successfully.")
            return pd.read_csv(io.StringIO(response.text), skiprows=1, low_memory=False)
        else:
            logging.error(f"Failed to fetch CSV data. Status code: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        logging.error(f"An error occurred while fetching CSV data: {e}")
        return pd.DataFrame()

# Function to save DataFrame to a CSV file
def save_csv_data(df, filename):
    try:
        df.to_csv(filename, index=False)
        logging.info(f"CSV data saved to {filename} successfully.")
    except Exception as e:
        logging.error(f"An error occurred while saving CSV data: {e}")

# Main execution
if __name__ == '__main__':
    logging.info("Starting CSV fetch and save process.")
    start_time = time.time()
    df = fetch_csv_data(csv_url)
    if not df.empty:
        save_csv_data(df, 'data.csv')
    end_time = time.time()
    logging.info(f"CSV fetch and save process completed in {end_time - start_time:.2f} seconds.")
    logging.info("CSV fetch and save process completed.")
