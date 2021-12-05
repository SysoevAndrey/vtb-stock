from dataclasses import dataclass, replace
from enum import Enum
from typing import Optional
from uuid import UUID

from loguru import logger


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
    available: bool = True

    def reserve(self) -> "Car":
        if self.available == False:
            logger.warning(f"Trying to reserve a reserved car - '{self.identifier}. Operation was not permitted.'")
            return self
        return replace(self, available=False)

    def free(self) -> "Car":
        if self.available == True:
            logger.warning(f"Trying to free a free car - '{self.identifier}. Operation was not permitted.'")
            return self
        return replace(self, available=True)
