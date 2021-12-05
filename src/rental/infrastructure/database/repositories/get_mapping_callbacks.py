from typing import Callable, Sequence

from rental.infrastructure.database.repositories.rental.sql_rental_mapping import bind_rentals_table_to_rental_model
from shared_kernel.database.connectors import SQLAlchemyDatabaseConnector


def get_mapping_callbacks() -> Sequence[Callable[[SQLAlchemyDatabaseConnector], None]]:
    return [
        bind_rentals_table_to_rental_model,
    ]
