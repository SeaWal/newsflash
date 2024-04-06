import json
from pathlib import Path

class WebScraper:
    def __init__(self, source_file: Path) -> None:
        self.source_file = source_file
        self.__load_sources()

    def scrape(self) -> None:
        pass

    def print_sources(self) -> None:
        for source in self.sources:
            print(f"Source: {source['source']}, Url: {source['url']}")

    def __load_sources(self) -> None:
        try:
            with open(self.source_file, 'r') as f:
                self.sources = json.load(f)['sources']
        except FileNotFoundError:
            print(f"Couldn't find file {self.source_file}.")
        except json.JSONDecodeError:
            print(f"Couldn't decode {self.source_file} as JSON.")

    def __fetch_page(self) -> None:
        pass

    def __parse_page(self) -> None:
        pass

    def __fetch_and_parse(self) -> None:
        pass


if __name__ == '__main__':
    path = Path(__file__).parent.parent / "sources.json"
    scraper = WebScraper(path)
    scraper.print_sources()