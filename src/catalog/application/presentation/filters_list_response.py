from typing import Optional
from pydantic import BaseModel, Field

from catalog.core.domain.available_parameter import ParameterType


class SortKeyResponse(BaseModel):
    id: str = Field(alias="id", example="cheaper")
    label: str = Field(alias="label", example="Сначала дешевле")


class SubCategoryResponse(BaseModel):
    id: str = Field(alias="id", example="electronics")
    label: str = Field(alias="label", example="Электроника")
    path: str = Field(alias="path", example="/api/products/filters?categories=electronics")


class CategoryResponse(BaseModel):
    id: str = Field(alias="id", example="electronics")
    label: str = Field(alias="label", example="Электроника")
    image: str = Field(alias="image", example="https://image.com/random-img")
    path: str = Field(alias="path", example="/api/products/filters?categories=electronics")

    sub_categories: list[SubCategoryResponse] = Field(alias="subCategories")


class ParameterStatsResponse(BaseModel):
    minimum: float = Field(alias="minimum", example=1000)
    maximum: float = Field(alias="maximum", example=10000)
    average: float = Field(alias="average", example=5000)
    total_sum: float = Field(alias="totalSum", example=100000)


class AvailableValueResponse(BaseModel):
    id: str = Field(alias="id", example="apple")
    label: str = Field(alias="label", example="Apple")
    doc_count: str = Field(alias="docCount", example=15)


class ParameterResponse(BaseModel):
    id: str = Field(alias="id", example="brand")
    label: str = Field(alias="label", example="Производитель")
    type: ParameterType = Field(alias="type", example=ParameterType.KEYWORD)
    stats: Optional[ParameterStatsResponse] = Field(alias="stats")
    available_values: list[AvailableValueResponse] = Field(alias="availableValues")


class FiltersListResponse(BaseModel):
    parameters: list[ParameterResponse] = Field(alias="parameters")
    categories: list[CategoryResponse] = Field(alias="categories")
    sort: list[SortKeyResponse] = Field(alias="sort")
