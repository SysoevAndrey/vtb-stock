from functools import partial
from time import sleep

import inject
from payment.core.domain.payment_repository import PaymentRepository
from payment.core.services.payment_list_service import PaymentListService
from payment.entrypoint.config import Config
from payment.infrastructure.database.repositories.payments.sql_payment_repository import PostgreSQLPaymentRepository
from payment.infrastructure.database.repositories.get_mapping_callbacks import get_mapping_callbacks
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
    inject_binder.bind_to_constructor(PaymentRepository, PostgreSQLPaymentRepository)  # type: ignore
    inject_binder.bind_to_constructor(PaymentListService, PaymentListService)  # type: ignore


def bind(config: Config):
    inject.configure_once(partial(_configure, config=config))
    if not config.is_debug:
        # Wait for injector
        sleep(10)
