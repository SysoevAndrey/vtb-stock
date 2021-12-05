from rental.core.domain.rental import Rental, RentalStatus
from shared_kernel.database.connectors.base_connector import SQLAlchemyDatabaseConnector
from sqlalchemy import Column, Enum, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper
from sqlalchemy.sql.sqltypes import Date


def bind_rentals_table_to_rental_model(database_connector: SQLAlchemyDatabaseConnector):
    rental_table = Table(
        "rental",
        database_connector.metadata,
        Column("identifier", UUID(as_uuid=True), primary_key=True),
        Column("user_id", String),
        Column("date_from", Date),
        Column("date_to", Date),
        Column("car_uid", UUID(as_uuid=True)),
        Column("status", Enum(RentalStatus)),
        Column("payment_uid", UUID(as_uuid=True)),
        extend_existing=True,
        schema=database_connector.schema,
    )

    mapper(Rental, rental_table)
