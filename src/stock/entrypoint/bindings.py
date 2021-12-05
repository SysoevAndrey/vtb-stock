from functools import partial
from time import sleep

import inject
from stock.core.domain.car_repository import CarRepository
from stock.core.services.car_list_service import CarListService
from stock.entrypoint.config import Config
from stock.infrastructure.database.repositories.cars import PostgreSQLCarRepository
from stock.infrastructure.database.repositories.get_mapping_callbacks import get_mapping_callbacks
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
        create_tables=config.create_tables,
    )
    inject_binder.bind(Config, config)
    inject_binder.bind_to_constructor(SQLAlchemyDatabaseConnector, lambda: database_connector)

    inject_binder.bind_to_constructor(DatabaseTransactionManager, DatabaseTransactionManager)  # type: ignore
    inject_binder.bind_to_constructor(CarRepository, PostgreSQLCarRepository)  # type: ignore
    inject_binder.bind_to_constructor(CarListService, CarListService)  # type: ignore


def bind(config: Config):
    inject.configure_once(partial(_configure, config=config))
    if not config.is_debug:
        # Wait for injector
        sleep(10)
