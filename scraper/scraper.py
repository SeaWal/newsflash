import json
from pathlib import Path
from typing import List

import aiohttp, asyncio
from bs4 import BeautifulSoup

from .article import Article

class WebScraper:
    def __init__(self, source_file: Path) -> None:
        self.source_file = source_file
        self.__load_sources()

    async def scrape(self) -> List[Article]:
        try:
            tasks = [self.__fetch_and_parse(source) for source in self.sources]
            results = await asyncio.gather(*tasks)
        except Exception as e:
            print(f"Exception occurred during scraping.")

    def print_sources(self) -> None:
        for source in self.sources:
            print(f"Source: {source['name']}, Url: {source['url']}")

    def __load_sources(self) -> None:
        try:
            with open(self.source_file, 'r') as f:
                self.sources = json.load(f)['sources']
        except FileNotFoundError:
            print(f"Couldn't find file {self.source_file}.")
        except json.JSONDecodeError:
            print(f"Couldn't decode {self.source_file} as JSON.")

    async def __fetch_page(self, url: str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()

    async def __parse_page(self, source, html: bytes) -> List[Article]:
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        parse_rules = source['parse_rules']
        for article_html in article_html.select(parse_rules['article_selector']):
            title = article_html.select_one(parse_rules['title_selector'])
            href = article_html.select_one(parse_rules['href_selector'])
            summary = article_html.select_one(parse_rules['summary_selector'])
            article = Article(title, href, summary)
            articles.append(article)
        return articles
    
    async def __fetch_and_parse(self, source) -> List[Article]:
        try:
            html = await self.__fetch_page(source['url'])
            return await self.__parse_page(source, html)
        except Exception as e:
            print(f"An error occurred while fetching and parsing {source['name']}.")

if __name__ == '__main__':
    path = Path(__file__).parent.parent / "sources.json"
    scraper = WebScraper(path)
    scraper.print_sources()