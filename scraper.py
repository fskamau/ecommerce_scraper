import requests
from bs4 import BeautifulSoup
import time
import logging
import csv
import os

class EcommerceScraper:
    """
    A robust web scraper designed to extract e-commerce data from books.toscrape.com.
    """
    
    def __init__(self, base_url="http://books.toscrape.com/catalogue/", pages_to_scrape=5):
        self.base_url = base_url
        self.pages_to_scrape = pages_to_scrape
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.data = []
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def fetch_page(self, url):
        """Fetches the HTML content of a given URL."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    def parse_books(self, html_content):
        """Parses book details from the provided HTML content."""
        soup = BeautifulSoup(html_content, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        
        for book in books:
            try:
                # Extract Title
                title = book.find('h3').find('a')['title']
                
                # Extract Price
                price_str = book.find('p', class_='price_color').text
                
                # Extract Rating (Class name contains the rating, e.g., 'star-rating Three')
                rating_p = book.find('p', class_='star-rating')
                rating = rating_p['class'][1] if rating_p else 'None'
                
                # Extract Availability
                availability = book.find('p', class_='instock availability').text.strip()
                
                self.data.append({
                    'Title': title,
                    'Price_Raw': price_str,
                    'Rating_Text': rating,
                    'Availability': availability
                })
            except AttributeError as e:
                self.logger.warning(f"Missing data on a book element: {e}")
                continue

    def run_scraper(self):
        """Executes the scraping loop across multiple pages."""
        self.logger.info(f"Starting scraping process for {self.pages_to_scrape} pages...")
        
        for page_num in range(1, self.pages_to_scrape + 1):
            url = f"{self.base_url}page-{page_num}.html"
            self.logger.info(f"Scraping {url}...")
            
            html = self.fetch_page(url)
            if html:
                self.parse_books(html)
            
            # Politeness delay to prevent server overload
            time.sleep(1)
            
        self.logger.info(f"Scraping complete. Extracted {len(self.data)} items.")
        return self.data

    def save_to_csv(self, filename="data/raw_books_data.csv"):
        """Saves the extracted data to a CSV file."""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        if not self.data:
            self.logger.warning("No data to save.")
            return
            
        keys = self.data[0].keys()
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.data)
            self.logger.info(f"Raw data saved successfully to {filename}")
        except IOError as e:
            self.logger.error(f"Error saving file: {e}")