from marshmallow import fields
from marshmallow_enum import EnumField
from payment.application.presentation import PresentationSchema
from payment.application.request_mapper.create_payment_request import CreatePaymentRequest
from payment.core.domain.payment import PaymentStatus
from pydantic import UUID4, Field


class PaymentResponse(CreatePaymentRequest):
    identifier: UUID4 = Field(alias="paymentUid")
    status: PaymentStatus = Field(alias="status")


class PaymentResponsePresentationSchema(PresentationSchema):
    __model__ = PaymentResponse.construct
    identifier = fields.UUID()
    status = EnumField(PaymentStatus, by_value=True)
    price = fields.Integer()
