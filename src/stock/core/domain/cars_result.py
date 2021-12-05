from dataclasses import dataclass
from typing import Iterable

from stock.core.domain.car import Car


@dataclass(frozen=True)
class CarsResult:
    total_count: int
    cars: list[Car]
