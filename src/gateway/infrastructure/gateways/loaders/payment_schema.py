from gateway.core.domain.payment import Payment, PaymentStatus
from gateway.infrastructure.gateways.loaders import LoaderSchema
from marshmallow import fields
from marshmallow_enum import EnumField


class PaymentLoaderSchema(LoaderSchema):
    __model__ = Payment
    identifier = fields.UUID(data_key="paymentUid")
    price = fields.Integer()
    status = EnumField(PaymentStatus, by_name=True)
