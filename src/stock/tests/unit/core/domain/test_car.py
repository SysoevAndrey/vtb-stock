from uuid import uuid4
import pytest
from stock.core.domain.car import CarType, Car


@pytest.mark.parametrize(
    "test_car,expected_car",
    [
        pytest.param(
            Car(
                identifier=uuid4(),
                brand="1",
                model="1",
                registration_number="1",
                power=123,
                type=CarType.SEDAN,
                price=240,
                available=True,
            ),
            Car(
                identifier=uuid4(),
                brand="1",
                model="1",
                registration_number="1",
                power=123,
                type=CarType.SEDAN,
                price=240,
                available=False,
            ),
        ),
        pytest.param(
            Car(
                identifier=uuid4(),
                brand="1",
                model="1",
                registration_number="1",
                power=123,
                type=CarType.SEDAN,
                price=240,
                available=False,
            ),
            Car(
                identifier=uuid4(),
                brand="1",
                model="1",
                registration_number="1",
                power=123,
                type=CarType.SEDAN,
                price=240,
                available=False,
            ),
        ),
    ],
)
def test_car_reserve(test_car: Car, expected_car: Car):
    changed_car = test_car.reserve()
    assert changed_car.available == expected_car.available


@pytest.mark.parametrize(
    "test_car,expected_car",
    [
        pytest.param(
            Car(
                identifier=uuid4(),
                brand="1",
                model="1",
                registration_number="1",
                power=123,
                type=CarType.SEDAN,
                price=240,
                available=True,
            ),
            Car(
                identifier=uuid4(),
                brand="1",
                model="1",
                registration_number="1",
                power=123,
                type=CarType.SEDAN,
                price=240,
                available=True,
            ),
        ),
        pytest.param(
            Car(
                identifier=uuid4(),
                brand="1",
                model="1",
                registration_number="1",
                power=123,
                type=CarType.SEDAN,
                price=240,
                available=False,
            ),
            Car(
                identifier=uuid4(),
                brand="1",
                model="1",
                registration_number="1",
                power=123,
                type=CarType.SEDAN,
                price=240,
                available=True,
            ),
        ),
    ],
)
def test_car_free(test_car: Car, expected_car: Car):
    changed_car = test_car.free()
    assert changed_car.available == expected_car.available
