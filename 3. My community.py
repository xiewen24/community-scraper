import requests
from bs4 import BeautifulSoup
import csv
import os

# Base URL of the website
BASE_URL = "https://www.mycommunitydirectory.com.au/New_South_Wales/Port_Macquarie-Hastings"

# Function to scrape details from the directory
def scrape_directory():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    entries = []
    for card in soup.find_all('div', class_='community-directory-item'):
        try:
            name = card.find('h3').text.strip()
            description = card.find('p').text.strip() if card.find('p') else "No description"
            link = card.find('a', href=True)['href'] if card.find('a', href=True) else "No link"

            entries.append({
                'Name': name,
                'Description': description,
                'Link': link,
            })
        except Exception as e:
            print(f"Error processing card: {e}")

    print(f"Scraped entries: {entries}")
    return entries

# Save data to a CSV file
def save_to_csv(data, filename):
    if not data:
        print("No data to save. Exiting.")
        return

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    filepath = os.path.join(desktop, filename)

    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    directory_entries = scrape_directory()
    save_to_csv(directory_entries, "community_directory.csv")
    print("Scraping complete! Data saved to your Desktop as community_directory.csv.")
