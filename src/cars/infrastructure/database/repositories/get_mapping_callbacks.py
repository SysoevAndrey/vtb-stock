from typing import Callable, Sequence

from cars.infrastructure.database.repositories.cars.sql_car_mapping import bind_cars_table_to_cars_model
from shared_kernel.database.connectors import SQLAlchemyDatabaseConnector


def get_mapping_callbacks() -> Sequence[Callable[[SQLAlchemyDatabaseConnector], None]]:
    return [
        bind_cars_table_to_cars_model,
    ]
