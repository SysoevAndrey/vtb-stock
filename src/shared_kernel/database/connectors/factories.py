from typing import Callable, Optional, Sequence
from shared_kernel.database.connectors.base_connector import SQLAlchemyDatabaseConnector
from shared_kernel.database.connectors.postgresql import PostgreSQLConnector


def get_postgresql_connector(
    database_url: str,
    database_connect_pool_recycle: int,
    database_connect_pool_size: int,
    mapping_callbacks: Sequence[Callable[[SQLAlchemyDatabaseConnector], None]],
    schema: Optional[str] = None,
    create_tables: bool = False,
) -> PostgreSQLConnector:
    database_connector = PostgreSQLConnector(
        database_url=database_url,
        database_connect_pool_size=database_connect_pool_size,
        database_connect_pool_recycle=database_connect_pool_recycle,
        schema=schema,
    )
    database_connector.prepare_db(mapping_callbacks, create_tables=create_tables)
    return database_connector
