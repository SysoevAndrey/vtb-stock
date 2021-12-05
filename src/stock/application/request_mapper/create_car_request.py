from typing import Optional

from stock.core.domain.car import CarType
from pydantic import BaseModel
from pydantic.fields import Field


class CreateCarRequest(BaseModel):
    brand: str = Field(alias="brand")
    model: str = Field(alias="model")
    registration_number: str = Field(alias="registrationNumber")
    power: Optional[int] = Field(alias="power")
    type: CarType = Field(alias="type")
    price: int = Field(alias="price")
