from dataclasses import dataclass
from typing import Optional

from catalog.core.domain.available_parameter import AvailableValue, ParameterStats


@dataclass(frozen=True)
class NumberParameterAgg:
    doc_count: int
    id: str
    label: str
    value_stats: ParameterStats


@dataclass(frozen=True)
class KeywordParameterAgg:
    doc_count: int
    id: str
    label: str
    available_values: list[AvailableValue]


@dataclass(frozen=True)
class SortKeyAgg:
    doc_count: int
    id: str
    label: str


@dataclass(frozen=True)
class CategoryAgg:
    doc_count: int
    id: str
    label: str
    image: str
    parent: Optional[str]


@dataclass(frozen=True)
class FiltersAggregationResult:
    number_parameters_aggs: list[NumberParameterAgg]
    keyword_parameters_aggs: list[KeywordParameterAgg]
    sort_key_aggs: list[SortKeyAgg]
    category_aggs: list[CategoryAgg]
