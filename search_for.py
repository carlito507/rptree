import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pydantic import BaseModel, validator
from typing import List, Set
import time
from textblob import TextBlob
from colorama import Fore

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
        # Remove all whitespace characters from the text
        text_without_whitespace = re.sub(r'\s', '', text)

        # Perform sentiment analysis using TextBlob
        analysis = TextBlob(text_without_whitespace)
        sentiment_polarity = analysis.sentiment.polarity

        # Interpret the sentiment polarity
        if sentiment_polarity > 0:
            sentiment = 'positive'
        elif sentiment_polarity < 0:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        # Print the results
        print(Fore.LIGHTMAGENTA_EX + f'Sentiment analysis for URL: {Fore.LIGHTGREEN_EX}{url}')
        print(Fore.LIGHTMAGENTA_EX + f'Sentiment polarity: {Fore.LIGHTYELLOW_EX}{sentiment_polarity}')
        print(Fore.LIGHTMAGENTA_EX + f'Sentiment: {Fore.LIGHTYELLOW_EX}{sentiment}' + Fore.RESET)

    def crawl(self, url: str, depth: int) -> None:
        if depth > self.max_depth or url in self.visited:
            return

        self.visited.add(url)

        # Print progress message for starting to crawl a new URL
        print(Fore.LIGHTMAGENTA_EX + f'Starting to crawl URL: {url} (depth: {Fore.LIGHTYELLOW_EX}{depth}{Fore.LIGHTMAGENTA_EX})' + Fore.RESET)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            if self.keyword.lower() in soup.text.lower():
                print(Fore.GREEN + f'Found keyword "{Fore.LIGHTGREEN_EX}{self.keyword}{Fore.GREEN}" at {Fore.LIGHTGREEN_EX}{url}' + Fore.RESET)
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
