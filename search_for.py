import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pydantic import BaseModel, validator
from typing import List, Set

class WebCrawler(BaseModel):
    seed_urls: List[str]
    keyword: str
    max_depth: int
    visited: Set[str] = set()

    @validator('max_depth')
    def validate_max_depth(cls, value):
        if value < 0:
            raise ValueError('max_depth must be non-negative')
        return value

    def crawl(self, url: str, depth: int) -> None:
        if depth > self.max_depth or url in self.visited:
            return

        self.visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            if self.keyword.lower() in soup.text.lower():
                print(f'Found keyword "{self.keyword}" at {url}')

            links = soup.find_all('a', href=True)

            for link in links:
                next_url = urljoin(url, link['href'])
                self.crawl(next_url, depth + 1)
        except Exception as e:
            print(f"Error while crawling {url}: {e}")

    def start_crawling(self) -> None:
        for seed_url in self.seed_urls:
            self.crawl(seed_url, 0)

# Example usage
crawler = WebCrawler(
    seed_urls=['https://bitcointalk.org/', 'https://www.reddit.com/r/Bitcoin/'],
    keyword='bitcoins',
    max_depth=2
)
crawler.start_crawling()
