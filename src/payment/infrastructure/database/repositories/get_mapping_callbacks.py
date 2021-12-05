from typing import Callable, Sequence

from payment.infrastructure.database.repositories.payments.sql_payment_mapping import (
    bind_payments_table_to_payment_model,
)
from shared_kernel.database.connectors import SQLAlchemyDatabaseConnector


def get_mapping_callbacks() -> Sequence[Callable[[SQLAlchemyDatabaseConnector], None]]:
    return [
        bind_payments_table_to_payment_model,
    ]
