from abc import ABCMeta
from dataclasses import dataclass
from typing import Optional, Type

from catalog.core.domain.card import Card


class NumberSortDescriptor:
    mapping = {
        "price": ("cheaper", "Сначала дешевле"),
        "rating": ("greater_rating", "Сначала с более высоким рейтингом"),
        "reviews_count": ("more_reviews", "Сначала с большим количеством отзывов"),
    }

    def __get__(self, instance: "CardDocument", owner: Type["CardDocument"]) -> list["NumberParameter"]:
        params = []
        for field, description in self.mapping.items():
            identifier, label = description
            value = getattr(instance.item, field)
            params.append(NumberParameter(id=identifier, label=label, value=value))

        return params


@dataclass(frozen=True)
class FacetedParameter(metaclass=ABCMeta):
    id: str
    label: str


@dataclass(frozen=True)
class NumberParameter(FacetedParameter):
    value: float


@dataclass(frozen=True)
class KeywordParameter(FacetedParameter):
    values: list[str]


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

    _number_sort_parameters = NumberSortDescriptor()

    @property
    def number_sort_parameters(self) -> list[NumberParameter]:
        return self._number_sort_parameters
