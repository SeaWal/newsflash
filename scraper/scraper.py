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
            results =  await asyncio.gather(*tasks)
            return [article for article_list in results for article in article_list]
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
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.read()
        except:
            print(f"Error while fetching page {url}.")

    async def __parse_page(self, source, html: bytes) -> List[Article]:
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        parse_rules = source['parse_rules']
        for article_html in soup.select(parse_rules['article_selector']):
            try:
                title = await self.__parse_selector(article_html, parse_rules['title_selector'])
                href = await self.__parse_selector(article_html, parse_rules['href_selector'])
                summary = await self.__parse_selector(article_html, parse_rules['summary_selector'])
                article = Article(title.contents[0], href['href'], summary.contents[0], source['topic'])
                articles.append(article)
            except Exception as e:
                print(f"Error while parsing page {source['url']}. {e}")
                continue
        return articles
    
    async def __fetch_and_parse(self, source) -> List[Article]:
        try:
            html = await self.__fetch_page(source['url'])
            return await self.__parse_page(source, html)
        except Exception as e:
            print(f"An error occurred while fetching and parsing {source['name']}. {e}")

    async def __parse_selector(self, html: bytes, selector: str) -> list | dict:
        try:
            return html.select_one(selector)
        except:
            print(f"An error occurred while attempting to parse {selector}")
            return []

if __name__ == '__main__':
    path = Path(__file__).parent.parent / "sources.json"
    scraper = WebScraper(path)
    scraper.print_sources()