import datetime

from pydantic import UUID4, BaseModel, Field


class CreateRentalRequest(BaseModel):
    car_uid: UUID4 = Field(alias="carUid")
    date_from: datetime.date = Field(alias="dateFrom")
    date_to: datetime.date = Field(alias="dateTo")
