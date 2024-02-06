import requests

# URL of the CSV data
CSV_URL = 'https://www.fxblue.com/users/compoundit/csv'

# Make a GET request to fetch the raw CSV data
response = requests.get(CSV_URL)

# Check if the request was successful
if response.status_code == 200:
    # Open a file in write-binary mode ('wb') for saving the CSV data
    with open('downloaded_data.csv', 'wb') as file:
        file.write(response.content)
    print("CSV data has been downloaded and saved as 'downloaded_data.csv'.")
else:
    print(f"Failed to fetch the CSV data. Status code: {response.status_code}")