from typing import Optional

from gateway.application.presentation import PresentationSchema
from gateway.core.domain.car import CarType
from marshmallow import fields
from marshmallow_enum import EnumField
from pydantic import BaseModel, Field
from pydantic.types import UUID4


class CarResponse(BaseModel):
    car_uid: UUID4 = Field(alias="carUid")
    available: bool = Field(alias="available")
    brand: str = Field(alias="brand")
    model: str = Field(alias="model")
    registration_number: str = Field(alias="registrationNumber")
    power: Optional[int] = Field(alias="power")
    type: CarType = Field(alias="type")
    price: int = Field(alias="price")


class CarListResponse(BaseModel):
    page: int = Field(alias="page")
    page_size: int = Field(alias="pageSize")
    total_elements: int = Field(alias="totalElements")
    items: list[CarResponse] = Field(alias="items")


class CarResponsePresentationSchema(PresentationSchema):
    __model__ = CarResponse.construct
    car_uid = fields.UUID(attribute="identifier")
    brand = fields.String()
    model = fields.String()
    registration_number = fields.String()
    power = fields.String()
    type = EnumField(CarType, by_value=True)
    price = fields.Integer()
    available = fields.Boolean()


class CarListResponsePresentationSchema(PresentationSchema):
    __model__ = CarListResponse.construct
    page = fields.Integer()
    page_size = fields.Integer()
    total_elements = fields.Integer(attribute="total_count")
    items = fields.List(fields.Nested(CarResponsePresentationSchema), attribute="result")
