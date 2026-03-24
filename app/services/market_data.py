from duckduckgo_search import DDGS
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class MarketDataService:
    def __init__(self):
        self.ddgs = DDGS()

    async def get_sector_news(self, sector: str) -> List[Dict[str, str]]:
        """
        Search for recent news and trends in a specific sector within India.
        """
        query = f"current trade opportunities and market trends in {sector} sector India 2024 2025"
        results = []
        try:
            # Using DuckDuckGo Search to find relevant news
            search_results = self.ddgs.text(query, max_results=10)
            for r in search_results:
                results.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "link": r.get("href", "")
                })
        except Exception as e:
            logger.error(f"Error fetching data from DuckDuckGo: {e}")
            
        return results

    async def scrape_content(self, url: str) -> str:
        """
        Scrape text content from a given URL.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    return soup.get_text(separator=' ', strip=True)[:2000] # Limit content
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
        return ""

market_data_service = MarketDataService()
