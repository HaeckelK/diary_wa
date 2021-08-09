from dataclasses import dataclass


@dataclass
class Article:
    id: int
    url: str
    date_added: int


@dataclass
class NewArticle:
    url: str
