import asyncio
from logging.config import fileConfig

from alembic import context
from stock.entrypoint.config import Config
from stock.infrastructure.database.repositories.get_mapping_callbacks import get_mapping_callbacks
from loguru import logger
from shared_kernel.database.connectors import get_postgresql_connector
from sqlalchemy import text

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name:
    fileConfig(config.config_file_name)
configuration = Config()
config.set_main_option("sqlalchemy.url", configuration.database_url)
logger.debug(f"Current configuration - {configuration.to_dict()}")


def get_db_connector():
    return get_postgresql_connector(
        database_connect_pool_recycle=configuration.database_connect_pool_recycle,
        database_connect_pool_size=configuration.database_connect_pool_size,
        database_url=configuration.database_url,
        mapping_callbacks=get_mapping_callbacks(),
        schema=configuration.database_schema,
    )


def get_metadata(connector):
    return connector.metadata


connector = get_db_connector()
target_metadata = get_metadata(connector)


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():

    async with connector.engine.connect() as connection:
        current_tenant = context.get_x_argument(as_dictionary=True).get("tenant")
        # set search path on the connection, which ensures that
        # PostgreSQL will emit all CREATE / ALTER / DROP statements
        # in terms of this schema by default
        # await connection.execute(text("set search_path to %s" % current_tenant))

        # # make use of non-supported SQLAlchemy attribute to ensure
        # # the dialect reflects tables in terms of the current tenant name
        # connection.dialect.default_schema_name = current_tenant
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table="_migrations",
            version_table_schema=configuration.database_schema,
            compare_type=True,
            include_schemas=True,
        )
        await connection.run_sync(do_run_migrations)  # type: ignore


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
