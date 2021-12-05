from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional
from uuid import UUID


class CarType(str, Enum):
    SEDAN = "SEDAN"
    SUV = "SUV"
    MINIVAN = "MINIVAN"
    ROADSTER = "ROADSTER"


@dataclass
class Car:
    identifier: UUID
    brand: str
    model: str
    registration_number: str
    power: Optional[int]
    type: CarType
    price: int
    available: bool


@dataclass(frozen=True)
class CarsResult:
    total_count: int
    result: Iterable[Car]
    page_size: int
    page: int
