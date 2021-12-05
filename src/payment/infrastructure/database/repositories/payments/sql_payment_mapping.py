from payment.core.domain.payment import Payment, PaymentStatus
from shared_kernel.database.connectors.base_connector import SQLAlchemyDatabaseConnector
from sqlalchemy import Column, Enum, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper
from sqlalchemy.sql.sqltypes import Integer


def bind_payments_table_to_payment_model(database_connector: SQLAlchemyDatabaseConnector):
    payment_table = Table(
        "payment",
        database_connector.metadata,
        Column("identifier", UUID(as_uuid=True), primary_key=True),
        Column("status", Enum(PaymentStatus), nullable=False),
        Column("price", Integer, nullable=False),
        extend_existing=True,
        schema=database_connector.schema,
    )

    mapper(Payment, payment_table)
