import datetime
from uuid import UUID

from gateway.infrastructure.gateways.loaders import LoaderSchema
from marshmallow import fields
from marshmallow_enum import EnumField
from pydantic import BaseModel
from gateway.core.domain.rental import RentalStatus


class RentalProjection(BaseModel):
    identifier: UUID
    status: RentalStatus
    date_from: datetime.date
    date_to: datetime.date
    car_uid: UUID
    payment_uid: UUID


class RentalProjectionSchema(LoaderSchema):
    __model__ = RentalProjection
    identifier = fields.UUID(data_key="rentalUid")
    user_id = fields.String(data_key="userId")
    status = EnumField(RentalStatus, by_value=True)
    date_from = fields.Date(data_key="dateFrom")
    date_to = fields.Date(data_key="dateTo")
    car_uid = fields.UUID(data_key="carUid")
    payment_uid = fields.UUID(data_key="paymentUid")
