import sqlite3
import requests
from bs4 import BeautifulSoup

def scrape_primes():
    print("Scraping Wikipedia for prime numbers...")
    # We will scrape the list of the first 100 primes from Wikipedia
    url = "https://en.wikipedia.org/wiki/List_of_prime_numbers"
    
    # adding headers, since wikipedia blocks requests with no headers
    headers = {'User-Agent': 'PrimeScraper/1.0 (https://mywebsite.com; me@example.com) python-requests/2.31.0'}
    response = requests.get(url, headers=headers)
    #print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the first table on the page
    table = soup.find('table', {'class': 'wikitable'})
    # print(table)
    
    primes = []
    # Extract the first 10 rows (just for this demo)
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if not cells:
            continue
        for cell in cells:
            text = cell.get_text(strip=True).replace(',', '')
            if text.isdigit():
                primes.append(int(text))
        '''         
        cols = row.find_all('td')
        if len(cols) > 0:
            prime_str = cols[0].text.strip().replace(',', '')
            try:
                primes.append(int(prime_str))
            except ValueError:
                pass
        '''
    return primes

def store_and_analyze(primes):
    if not primes:
        print("No primes found.")
        return

    print(f"Found {len(primes)} primes. Storing in SQLite database...")
    # Connect to SQLite (this creates a file named primes.db if it doesn't exist)
    conn = sqlite3.connect('primes.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS prime_numbers (
                        id INTEGER PRIMARY KEY,
                        prime_value INTEGER
                    )''')

    # Insert data
    for p in primes:
        cursor.execute("INSERT INTO prime_numbers (prime_value) VALUES (?)", (p,))
    
    conn.commit()

    # Run a SQL query to analyze the data
    print("\n--- SQL Analysis ---")
    cursor.execute("SELECT COUNT(*), AVG(prime_value), MAX(prime_value) FROM prime_numbers")
    count, average, max_val = cursor.fetchone()
    
    print(f"Total Primes Stored: {count}")
    print(f"Average Value: {average}")
    print(f"Max Prime: {max_val}")

    conn.close()

if __name__ == "__main__":
    prime_list = scrape_primes()
    store_and_analyze(prime_list)
