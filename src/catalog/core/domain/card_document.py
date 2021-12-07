import json
from dataclasses import asdict, dataclass
from typing import Optional

from catalog.core.domain.card import Card


@dataclass(frozen=True)
class NumberParameter:
    id: str
    value: float

    @property
    def facet_info(self) -> str:
        return json.dumps({"id": self.id, "label": self.id})

    @property
    def facet_value(self) -> str:
        return json.dumps({"id": self.value, "label": self.value})


@dataclass(frozen=True)
class KeywordParameter:
    id: str
    values: list[str]

    @property
    def facet_info(self) -> str:
        return json.dumps({"id": self.id, "label": self.id})

    @property
    def facet_value(self) -> str:
        return json.dumps([{"id": value, "label": value} for value in self.values])


@dataclass(frozen=True)
class CardCategory:
    id: str
    parent: Optional[str]
    image: str
    label: str


@dataclass(frozen=True)
class CardDocument:
    item: Card
    type: str
    number_parameters: list[NumberParameter]
    keyword_parameters: list[KeywordParameter]
    categories: list[CardCategory]

    @property
    def categories_info(self) -> list[str]:
        return []  # FIXME

    @property
    def search_result(self) -> dict[str, str]:
        return {key: str(value) for key, value in asdict(self.item).items()}

    @property
    def number_search_data(self) -> dict[str, float]:
        return {parameter.id: parameter.value for parameter in self.number_parameters}

    @property
    def keyword_search_data(self) -> dict[str, list[str]]:
        return {parameter.id: parameter.values for parameter in self.keyword_parameters}
