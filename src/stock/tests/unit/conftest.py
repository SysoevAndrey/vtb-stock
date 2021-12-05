import asyncio

import inject
import pytest
from stock.entrypoint.bindings import bind
from stock.entrypoint.config import TestConfig
from pytest_postgresql.janitor import DatabaseJanitor


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
@pytest.mark.asyncio
def configuration():
    conf = TestConfig()
    print(f"Test configuration is {conf.to_dict()}")
    return conf


@pytest.fixture(scope="session")
@pytest.mark.asyncio
def database(configuration: TestConfig):
    with DatabaseJanitor(
        host=configuration.database_host,
        port=configuration.database_port,
        user=configuration.database_user,
        password=configuration.database_password,
        dbname=configuration.database_name,
        version=11,
    ):
        yield


@pytest.mark.usefixtures("database")
@pytest.mark.asyncio
@pytest.fixture(scope="session")
async def inject_dependencies(configuration: TestConfig):
    bind(configuration)
