from pathlib import Path
import asyncio

from scraper import WebScraper


async def main():
    path = Path(__file__).parent / "sources.json"
    scraper = WebScraper(path)
    await scraper.scrape()

if __name__ == '__main__':
    asyncio.run(main())