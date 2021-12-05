from pydantic import BaseModel, Field


class CreatePaymentRequest(BaseModel):
    price: int = Field(alias="price")
