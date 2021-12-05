import datetime

from marshmallow import fields
from marshmallow_enum import EnumField
from pydantic import Field
from pydantic.types import UUID4
from rental.application.presentation import PresentationSchema
from rental.application.request_mapper.create_rental_request import CreateRentalRequest
from rental.core.domain.rental import RentalStatus


class RentalResponse(CreateRentalRequest):
    rental_uid: UUID4 = Field(alias="rentalUid")
    status: RentalStatus = Field(alias="status")
    date_from: datetime.date = Field(alias="dateFrom")
    date_to: datetime.date = Field(alias="dateTo")
    car_uid: UUID4 = Field(alias="carUid")
    payment_uid: UUID4 = Field(alias="paymentUid")


class RentalResponsePresentationSchema(PresentationSchema):
    __model__ = RentalResponse.construct
    rental_uid = fields.UUID(attribute="identifier")
    status = EnumField(RentalStatus, by_value=True)
    date_from = fields.Date()
    date_to = fields.Date()
    car_uid = fields.UUID()
    payment_uid = fields.UUID()
