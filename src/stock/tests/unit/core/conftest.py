from uuid import UUID
import inject
import pytest
from stock.core.domain.car import Car, CarType
from stock.infrastructure.database.repositories.cars.sql_car_repository import PostgreSQLCarRepository
from shared_kernel.database.transaction import async_transactional


@pytest.mark.usefixtures("inject_dependencies")
@pytest.fixture(scope="module")
@pytest.mark.asyncio
async def insert_data_to_test_db():
    async def _insert(repo, data):
        await repo.create_tables()
        for item in data:
            await repo.save(item)

    repository = inject.instance(PostgreSQLCarRepository)

    data = [
        Car(
            identifier=UUID("4970cb2b-d82b-4cea-a848-4db44e97e3f6"),
            brand="test1",
            model="test1",
            registration_number="test1",
            power=240,
            type=CarType.SEDAN,
            price=240,
            available=True,
        ),
        Car(
            identifier=UUID("9871eb2a-4dff-49ce-a4b6-2f9fe1775e03"),
            brand="test2",
            model="test2",
            registration_number="test2",
            power=240,
            type=CarType.SEDAN,
            price=240,
            available=True,
        ),
        Car(
            identifier=UUID("102a39b6-3fd8-499d-a38f-751d319776bc"),
            brand="test3",
            model="test3",
            registration_number="test3",
            power=240,
            type=CarType.SEDAN,
            price=240,
            available=True,
        ),
        Car(
            identifier=UUID("0e52b0a9-2c68-4275-984e-a085d7727aa3"),
            brand="test4",
            model="test4",
            registration_number="test4",
            power=240,
            type=CarType.SEDAN,
            price=240,
            available=True,
        ),
        Car(
            identifier=UUID("45553445-431c-411d-9549-d50969ed5461"),
            brand="test5",
            model="test5",
            registration_number="test5",
            power=240,
            type=CarType.SEDAN,
            price=240,
            available=True,
        ),
        Car(
            identifier=UUID("f3f7e169-ef65-43f8-8c05-97f727595f15"),
            brand="test5",
            model="test5",
            registration_number="test5",
            power=240,
            type=CarType.SEDAN,
            price=240,
            available=False,
        ),
    ]
    await async_transactional(_insert)(repository, data)
