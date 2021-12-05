from datetime import date
from uuid import uuid4

import pytest
from rental.core.domain.rental import Rental, RentalStatus


@pytest.mark.parametrize(
    "test_rental,status,expected_rental",
    [
        pytest.param(
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
            ),
            RentalStatus.IN_PROGRESS,
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.IN_PROGRESS,
            ),
        ),
        pytest.param(
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.IN_PROGRESS,
            ),
            RentalStatus.CANCELED,
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.CANCELED,
            ),
        ),
        pytest.param(
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
            ),
            RentalStatus.CANCELED,
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.CANCELED,
            ),
        ),
        pytest.param(
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.CANCELED,
            ),
            RentalStatus.IN_PROGRESS,
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.CANCELED,
            ),
        ),
        pytest.param(
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.IN_PROGRESS,
            ),
            RentalStatus.FINISHED,
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.FINISHED,
            ),
        ),
        pytest.param(
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
            ),
            RentalStatus.FINISHED,
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.FINISHED,
            ),
        ),
        pytest.param(
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.FINISHED,
            ),
            RentalStatus.NEW,
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.FINISHED,
            ),
        ),
        pytest.param(
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.FINISHED,
            ),
            RentalStatus.IN_PROGRESS,
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.FINISHED,
            ),
        ),
        pytest.param(
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.CANCELED,
            ),
            RentalStatus.NEW,
            Rental(
                identifier=uuid4(),
                user_id="1",
                date_from=date(2021, 12, 3),
                date_to=date(2021, 12, 4),
                car_uid=uuid4(),
                payment_uid=uuid4(),
                status=RentalStatus.CANCELED,
            ),
        ),
    ],
)
def test_rental_set_status(test_rental: Rental, status: RentalStatus, expected_rental: Rental):
    changed_rental = test_rental.set_status(status)
    assert changed_rental.status == expected_rental.status
