# crawler.py
import requests
from bs4 import BeautifulSoup
from .config import MAX_DEPTH
from .utils import save_to_database

class WebCrawler:
    def __init__(self):
        self.visited_urls = set()

    def crawl(self, url, depth=0):
        if depth > MAX_DEPTH or url in self.visited_urls:
            return
        try:
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.text
                # Parse HTML using BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                # Extract relevant information or store the HTML content as needed
                save_to_database(url, html_content)
                self.visited_urls.add(url)
                # Extract and follow links for recursive crawling
                for link in soup.find_all('a', href=True):
                    next_url = link['href']
                    self.crawl(next_url, depth + 1)
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")
