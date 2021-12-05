import datetime
from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from gateway.core.domain.car import Car
from gateway.core.domain.payment import Payment


class RentalStatus(Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"


@dataclass
class Rental:
    identifier: UUID
    status: RentalStatus
    date_from: datetime.date
    date_to: datetime.date
    car: Car
    payment: Payment
