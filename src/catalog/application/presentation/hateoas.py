from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.networks import HttpUrl


class Link(BaseModel):
    href: HttpUrl = Field(
        alias="href",
        example="https://vtb-stock.com/catalog/api/cards?sort=cheaper&categories=electronics,smartphones&filters=minPrice=1000,maxPrice=10000&page=1&size=10",
    )
    path: str = Field(
        alias="path",
        example="/catalog/api/cards?sort=cheaper&categories=electronics,smartphones&filters=minPrice=1000,maxPrice=10000&page=1&size=10",
    )


class HateoasLinks(BaseModel):
    prev: Optional[Link] = Field(alias="prev")
    self_: Link = Field(alias="self")
    next_: Optional[Link] = Field(alias="next")
