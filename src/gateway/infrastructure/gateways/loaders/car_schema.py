from gateway.core.domain.car import Car, CarType, CarsResult
from gateway.infrastructure.gateways.loaders import LoaderSchema
from marshmallow import fields
from marshmallow_enum import EnumField


class CarLoaderSchema(LoaderSchema):
    __model__ = Car
    identifier = fields.UUID(data_key="carUid")
    brand = fields.String(data_key="brand")
    model = fields.String(data_key="model")
    registration_number = fields.String(data_key="registrationNumber")
    power = fields.Integer(data_key="power")
    type = EnumField(CarType, by_value=True, data_key="type")
    price = fields.Integer(data_key="price")
    available = fields.Boolean(data_key="available")


class CarResultLoaderSchema(LoaderSchema):
    __model__ = CarsResult
    total_count = fields.Integer(data_key="totalElements")
    result = fields.List(fields.Nested(CarLoaderSchema), data_key="items")
    page_size = fields.Integer(data_key="pageSize")
    page = fields.Integer(data_key="page")
