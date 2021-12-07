from dataclasses import dataclass
from catalog.core.domain.category import Category
from catalog.core.domain.available_parameter import AvailableParameter
from catalog.core.domain.sort_key import SortKey


@dataclass(frozen=True)
class FiltersResult:
    parameters: list[AvailableParameter]
    categories: list[Category]
    sort: list[SortKey]
