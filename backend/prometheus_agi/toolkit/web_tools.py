import requests
from bs4 import BeautifulSoup
from .base_tool import BaseTool

class WebScraper(BaseTool):
    name = "web_scraper"
    description = "Scrapes the headlines from a given URL."
    def run(self, url: str) -> dict:
        print(f"  > Scraping content from {url}...")
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if response.status_code != 200:
                return {"error": f"HTTP status code {response.status_code}"}
            soup = BeautifulSoup(response.content, 'html.parser')
            headlines = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])]
            return {"url": url, "headlines": headlines}
        except Exception as e:
            return {"error": f"Could not scrape URL {url}: {e}"}