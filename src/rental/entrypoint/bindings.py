from functools import partial
from time import sleep

import inject
from rental.core.domain.rental_repository import RentalRepository
from rental.core.services.rental_list_service import RentalListService
from rental.entrypoint.config import Config
from rental.infrastructure.database.repositories.rental.sql_rental_repository import PostgreSQLRentalRepository
from rental.infrastructure.database.repositories.get_mapping_callbacks import get_mapping_callbacks
from shared_kernel.database.connectors import SQLAlchemyDatabaseConnector, get_postgresql_connector
from shared_kernel.database.transaction.manager import DatabaseTransactionManager


def _configure(inject_binder: inject.Binder, config: Config):
    mappings = get_mapping_callbacks()
    database_connector = get_postgresql_connector(
        config.database_url,
        database_connect_pool_recycle=config.database_connect_pool_recycle,
        database_connect_pool_size=config.database_connect_pool_size,
        mapping_callbacks=mappings,
        schema=config.database_schema,
    )
    inject_binder.bind(Config, config)
    inject_binder.bind(SQLAlchemyDatabaseConnector, database_connector)

    inject_binder.bind_to_constructor(DatabaseTransactionManager, DatabaseTransactionManager)  # type: ignore
    inject_binder.bind_to_constructor(RentalRepository, PostgreSQLRentalRepository)  # type: ignore
    inject_binder.bind_to_constructor(RentalListService, RentalListService)  # type: ignore


def bind(config: Config):
    inject.configure_once(partial(_configure, config=config))
    if not config.is_debug:
        # Wait for injector
        sleep(10)
