from __future__ import annotations

from typing import Optional

from marshmallow import fields
from marshmallow_enum import EnumField
from pydantic import BaseModel, Field

from catalog.application.presentation import PresentationSchema
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

    sub_categories: list[CategoryResponse] = Field(alias="subCategories")


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


class ParametersStatsResponsePresentationSchema(PresentationSchema):
    __model__ = ParameterStatsResponse.construct
    minimum = fields.Float()
    maximum = fields.Float()
    average = fields.Float()
    total_sum = fields.Float()


class AvailableValueResponsePresentationSchema(PresentationSchema):
    __model__ = AvailableValueResponse.construct

    id = fields.String()
    label = fields.String()
    doc_count = fields.Integer()


class CategoryResponsePresentationSchema(PresentationSchema):
    __model__ = CategoryResponse.construct
    id = fields.String()
    label = fields.String()
    image = fields.String()

    sub_categories = fields.List(fields.Nested(lambda: CategoryResponsePresentationSchema()))


class SortKeyResponsePresentationSchema(PresentationSchema):
    __model__ = SortKeyResponse.construct

    id = fields.String()
    label = fields.String()


class ParameterResponsePresentationSchema(PresentationSchema):
    __model__ = ParameterResponse.construct

    id = fields.String()
    label = fields.String()
    type = EnumField(ParameterType, by_value=True)
    stats = fields.Nested(ParametersStatsResponsePresentationSchema, allow_none=True)
    available_values = fields.List(fields.Nested(AvailableValueResponsePresentationSchema))


class FiltersListResponsePresentationSchema(PresentationSchema):
    __model__ = FiltersListResponse.construct

    parameters = fields.List(fields.Nested(ParameterResponsePresentationSchema))
    categories = fields.List(fields.Nested(CategoryResponsePresentationSchema))
    sort = fields.List(fields.Nested(SortKeyResponsePresentationSchema))


CategoryResponse.update_forward_refs()
