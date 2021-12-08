from pydantic import BaseModel, Field
from pydantic.networks import HttpUrl
from pydantic.types import UUID4

from catalog.core.domain.available_parameter import ParameterType


class CardCreateRequest(BaseModel):
    id: UUID4 = Field(alias="id", example="382357c8-8547-41d1-9171-d23078dbfb60")
    image: HttpUrl = Field(alias="image", example="https://img.com/random")
    price: int = Field(alias="price", example=140000)
    label: str = Field(alias="label", example="Iphone 13")
    rating: float = Field(alias="rating", example=4.5)
    reviews_count: int = Field(alias="reviewsCount", example=49)
    path: str = Field(alias="path", example="/stock/electronics/382357c8-8547-41d1-9171-d23078dbfb60")


class NumberParameterCreateRequest(BaseModel):
    id: str = Field(alias="id", example="price")
    label: str = Field(alias="label", example="Цена")
    value: float = Field(alias="value", example=140000)


class KeywordParameterCreateRequest(BaseModel):
    id: str = Field(alias="id", example="brand")
    label: str = Field(alias="label", example="Производитель")
    values: list[str] = Field(alias="values", example=["Apple", "Samsung"])


class CardCategoryCreateRequest(BaseModel):
    id: str = Field(alias="id", example="electronics")
    image: HttpUrl = Field(alias="image", example="https://img.com/random")
    label: str = Field(alias="label", example="Электроника")


class CardDocumentCreateRequest(BaseModel):
    item: CardCreateRequest = Field(alias="item")
    number_parameters: list[NumberParameterCreateRequest] = Field(alias="numberParameters")
    keyword_parameters: list[KeywordParameterCreateRequest] = Field(alias="keywordParameters")
    categories: list[CardCategoryCreateRequest] = Field(alias="categories")
