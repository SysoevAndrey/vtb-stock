import datetime

from gateway.application.presentation import PresentationSchema
from gateway.core.domain.payment import PaymentStatus
from gateway.core.domain.rental import RentalStatus
from marshmallow import fields
from marshmallow_enum import EnumField
from pydantic import Field
from pydantic.main import BaseModel
from pydantic.types import UUID4


class CarRentalProjectionResponse(BaseModel):
    car_uid: UUID4 = Field(alias="carUid")
    brand: str = Field(alias="brand")
    model: str = Field(alias="model")
    registration_number: str = Field(alias="registrationNumber")


class PaymentResponse(BaseModel):
    payment_uid: UUID4 = Field(alias="paymentUid")
    status: PaymentStatus = Field(alias="status")
    price: int = Field(alias="price")


class RentalResponse(BaseModel):
    rental_uid: UUID4 = Field(alias="rentalUid")
    status: RentalStatus = Field(alias="status")
    date_from: datetime.date = Field(alias="dateFrom")
    date_to: datetime.date = Field(alias="dateTo")
    car: CarRentalProjectionResponse = Field(alias="car")
    payment: PaymentResponse = Field(alias="payment")


class PayedRentalResponse(BaseModel):
    rental_uid: UUID4 = Field(alias="rentalUid")
    status: RentalStatus = Field(alias="status")
    date_from: datetime.date = Field(alias="dateFrom")
    date_to: datetime.date = Field(alias="dateTo")
    car_uid: UUID4 = Field(alias="carUid")
    payment: PaymentResponse = Field(alias="payment")


class CarResponsePresentationSchema(PresentationSchema):
    __model__ = CarRentalProjectionResponse.construct
    car_uid = fields.UUID(attribute="identifier")
    brand = fields.String()
    model = fields.String()
    registration_number = fields.String()


class PaymentResponsePresentationSchema(PresentationSchema):
    __model__ = PaymentResponse.construct
    payment_uid = fields.UUID(attribute="identifier")
    status = EnumField(PaymentStatus, by_value=True)
    price = fields.Integer()


class RentalResponsePresentationSchema(PresentationSchema):
    __model__ = RentalResponse.construct
    rental_uid = fields.UUID(attribute="identifier")
    status = EnumField(RentalStatus, by_value=True)
    date_from = fields.Date()
    date_to = fields.Date()
    car = fields.Nested(CarResponsePresentationSchema)
    payment = fields.Nested(PaymentResponsePresentationSchema)


class PayedRentalResponsePresnetationSchema(PresentationSchema):
    __model__ = PayedRentalResponse.construct
    rental_uid = fields.UUID(attribute="identifier")
    status = EnumField(RentalStatus, by_value=True)
    date_from = fields.Date()
    date_to = fields.Date()
    car_uid = fields.UUID()
    payment = fields.Nested(PaymentResponsePresentationSchema)
