from dataclasses import dataclass

@dataclass
class Article:
    title: str
    href: str
    summary: str
    topic: str