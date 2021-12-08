from marshmallow import fields
from pydantic import BaseModel
from pydantic.fields import Field

from catalog.application.presentation import PresentationSchema


class SaveCardsResponseModel(BaseModel):
    success_count: int = Field(alias="successCount")
    failed_count: int = Field(alias="failedCount")


class SaveCardsResponseModelPresentationSchema(PresentationSchema):
    __model__ = SaveCardsResponseModel.construct

    success_count = fields.Integer()
    failed_count = fields.Integer()
