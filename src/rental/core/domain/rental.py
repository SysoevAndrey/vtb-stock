import datetime
from dataclasses import dataclass, replace
from enum import Enum
from typing import Iterable, Mapping, Type
from uuid import UUID

from loguru import logger


class RentalStatus(Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"


class RentalStateMachine:
    allowed_transformations: Mapping[RentalStatus, Iterable[RentalStatus]] = {
        RentalStatus.NEW: [RentalStatus.IN_PROGRESS, RentalStatus.CANCELED, RentalStatus.FINISHED],
        RentalStatus.IN_PROGRESS: [RentalStatus.FINISHED, RentalStatus.CANCELED],
        RentalStatus.CANCELED: [RentalStatus.FINISHED],
    }

    def __get__(self, instance: "Rental", owner: Type["Rental"]) -> Iterable[RentalStatus]:
        return self.allowed_transformations.get(instance.status, tuple())


@dataclass
class Rental:
    identifier: UUID
    user_id: str
    date_from: datetime.date
    date_to: datetime.date
    car_uid: UUID
    payment_uid: UUID
    status: RentalStatus = RentalStatus.IN_PROGRESS

    _next_statuses = RentalStateMachine()

    @property
    def next_statuses(self) -> Iterable[RentalStatus]:
        return self._next_statuses

    def set_status(self, status: RentalStatus) -> "Rental":
        if status in self.next_statuses:
            logger.debug(
                f"Rental - '{self.identifier}' move to next state - '{status.value}'. Previous state - '{self.status.value}'"
            )
            return replace(self, status=status)
        logger.debug(
            f"Rental - '{self.identifier}' can't move to next state - '{status.value}'. Rollback to '{self.status.value}'"
        )
        return self
