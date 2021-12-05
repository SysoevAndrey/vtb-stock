import datetime
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Optional, Tuple
from uuid import UUID

from stock.core.domain.car import Car


@dataclass(frozen=True)
class Error:
    reason: str
    timestamp: datetime.datetime = datetime.datetime.now()


class CarRepository(metaclass=ABCMeta):
    @abstractmethod
    async def filter_cars_by_availability(self, skip: int, limit: int, availability: bool) -> Tuple[Iterable[Car], int]:
        pass

    @abstractmethod
    async def list(self, skip: int, limit: int) -> Tuple[Iterable[Car], int]:
        pass

    @abstractmethod
    async def save(self, car: Car):
        pass

    @abstractmethod
    async def get_car_by_id(self, identifier: UUID, available: bool | str = True) -> Optional[Car]:
        pass

    @abstractmethod
    async def update_car(self, car: Car):
        pass
