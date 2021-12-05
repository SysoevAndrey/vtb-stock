from stock.core.domain import Car, CarType
from shared_kernel.database.connectors.base_connector import SQLAlchemyDatabaseConnector
from sqlalchemy import Boolean, Column, Enum, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper


def bind_cars_table_to_cars_model(database_connector: SQLAlchemyDatabaseConnector):
    car_table = Table(
        "cars",
        database_connector.metadata,
        Column("identifier", UUID(as_uuid=True), primary_key=True),
        Column("brand", String, nullable=False),
        Column("model", String, nullable=False),
        Column("registration_number", String, nullable=False),
        Column("power", Integer, nullable=True),
        Column("type", Enum(CarType), nullable=False),
        Column("price", Integer, nullable=False),
        Column("available", Boolean, nullable=False),
        extend_existing=True,
        schema=database_connector.schema,
    )

    mapper(Car, car_table)
