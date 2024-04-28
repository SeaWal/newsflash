from pathlib import Path
import asyncio

from scraper import WebScraper
from web import app

async def main():
    path = Path(__file__).parent / "sources.json"
    scraper = WebScraper(path)
    results = await scraper.scrape()
    
    app.articles = results
    app.run()

if __name__ == '__main__':
    asyncio.run(main())