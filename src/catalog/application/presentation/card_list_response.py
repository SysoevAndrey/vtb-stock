from marshmallow import fields
from pydantic import BaseModel, HttpUrl
from pydantic.fields import Field
from pydantic.types import UUID4

from catalog.application.presentation import PresentationSchema


class CardResponse(BaseModel):
    id: UUID4 = Field(alias="id", example="382357c8-8547-41d1-9171-d23078dbfb60")
    label: str = Field(alias="label", example="Iphone 13")
    image: HttpUrl = Field(alias="image", example="https://img.com/random")
    price: int = Field(alias="price", example=140000)
    rating: float = Field(alias="rating", example=4.5)
    reviews_count: int = Field(alias="reviewsCount", example=49)
    path: str = Field(alias="path", example="/stock/electronics/382357c8-8547-41d1-9171-d23078dbfb60")


class CardsPaginatedResponse(BaseModel):
    items: list[CardResponse] = Field(alias="items")
    total_elements: int = Field(alias="totalElements")


class CardResponsePresentationSchema(PresentationSchema):
    __model__ = CardResponse.construct
    id = fields.UUID()
    label = fields.String()
    image = fields.String()
    price = fields.Integer()
    rating = fields.Float()
    reviews_count = fields.Integer()
    path = fields.String()


class CardsPaginatedResponsePresentationSchema(PresentationSchema):
    __model__ = CardsPaginatedResponse.construct
    items = fields.List(fields.Nested(CardResponsePresentationSchema))
    total_elements = fields.Integer()
