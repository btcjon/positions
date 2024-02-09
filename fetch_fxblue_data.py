import requests
from bs4 import BeautifulSoup

def fetch_and_parse(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print("Failed to retrieve the webpage")
        return None

def extract_stats(soup):
    # Find the table by its class
    table = soup.find('table', class_='DataTable')
    if table:
        stats = {}
        # Iterate through each row in the table
        for row in table.find_all('tr')[1:]:  # Skip the header row with [1:]
            columns = row.find_all('td')
            if len(columns) >= 2:  # Ensure there are enough columns for key-value pairs
                # Assuming the first column is the stat name and the second is the value
                stat_name = row.find('th').text.strip()
                stat_value = columns[0].text.strip()
                # Store the data
                stats[stat_name] = stat_value
        return stats
    else:
        print("Table not found.")
        return {}

def main():
    url = "https://www.fxblue.com/users/compoundit/"  # Example URL
    soup = fetch_and_parse(url)
    if soup:
        stats = extract_stats(soup)
        for stat, value in stats.items():
            print(f"{stat}: {value}")

if __name__ == "__main__":
    main()
