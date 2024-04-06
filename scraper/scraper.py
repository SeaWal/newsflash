import json
from pathlib import Path

class WebScraper:
    def __init__(self, source_file: Path) -> None:
        self.source_file = source_file

    def scrape(self) -> None:
        pass

    def __load_source(self) -> None:
        pass

    def __fetch_page(self) -> None:
        pass

    def __parse_page(self) -> None:
        pass

    def __fetch_and_parse(self) -> None:
        pass
