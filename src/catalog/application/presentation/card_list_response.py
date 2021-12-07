from pydantic import BaseModel, HttpUrl
from pydantic.fields import Field
from pydantic.types import UUID4

from catalog.application.presentation.hateoas import HateoasLinks


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
    links: HateoasLinks = Field(alias="_links")
