import datetime

from pydantic import BaseModel, Field
from pydantic.types import UUID4


class CreateRentalRequest(BaseModel):
    date_from: datetime.date = Field(alias="dateFrom")
    date_to: datetime.date = Field(alias="dateTo")
    car_uid: UUID4 = Field(alias="carUid")
    payment_uid: UUID4 = Field(alias="paymentUid")
