import requests
import psycopg2
from bs4 import BeautifulSoup

# Database connection settings
DB_CONFIG = {
    "dbname": "your_database",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}



# Function to scrape data from a website
def scrape_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Example: Scraping a list of items with titles and prices
    data = []
    for item in soup.select(".product"):  # Adjust the selector as per the website structure
        title = item.select_one(".title").text.strip()
        price = float(item.select_one(".price").text.replace("$", "").strip())
        
        data.append({"title": title, "price": price})
    
    return data

# Function to filter data based on a price threshold
def filter_data(data, price_threshold=50):
    return [item for item in data if item["price"] <= price_threshold]

# Function to insert data into PostgreSQL database
def insert_into_db(data):
    if not data:
        print("No data to insert")
        return
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.executemany(
            "INSERT INTO products (title, price) VALUES (%s, %s)",
            [(item["title"], item["price"]) for item in data]
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Data inserted successfully")
    except Exception as e:
        print("Database error:", e)

if __name__ == "__main__":
    url = "https://example.com/products"  # Replace with actual URL
    scraped_data = scrape_data(url)
    filtered_data = filter_data(scraped_data, price_threshold=50)
    insert_into_db(filtered_data)
