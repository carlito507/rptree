import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pydantic import BaseModel, validator
from typing import List, Set
import time
import re


class WebCrawler(BaseModel):
    seed_urls: List[str]
    keyword: str
    max_depth: int
    visited: Set[str] = set()
    delay: float = 1.0  # Delay between requests in seconds

    @validator('max_depth')
    def validate_max_depth(cls, value):
        if value < 0:
            raise ValueError('max_depth must be non-negative')
        return value

    def process_text(self, url: str, text: str) -> None:
        # This method processes the extracted text from the page.
        # You can implement any text processing or analysis logic here.
        print(f'Processing text from URL: {url}')
        # print(text.replace("\n", "").replace("\t", "|").encode("utf-8"))
        text = re.sub(r'\s', '', text)
        print(text)


    def crawl(self, url: str, depth: int) -> None:
        if depth > self.max_depth or url in self.visited:
            return

        self.visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            if self.keyword.lower() in soup.text.lower():
                print(f'Found keyword "{self.keyword}" at {url}')
                self.process_text(url, soup.text)

            links = soup.find_all('a', href=True)

            for link in links:
                next_url = urljoin(url, link['href'])
                self.crawl(next_url, depth + 1)

                # Introduce a delay between requests to respect rate limits
                time.sleep(self.delay)
        except Exception as e:
            print(f"Error while crawling {url}: {e}")

    def start_crawling(self) -> None:
        for seed_url in self.seed_urls:
            self.crawl(seed_url, 0)


# Example usage
crawler = WebCrawler(
    seed_urls=['https://bitcointalk.org/', 'https://www.reddit.com/r/Bitcoin/'],
    keyword='bitcoins',
    max_depth=2,
    delay=2.0  # Delay of 2 seconds between requests
)
crawler.start_crawling()
