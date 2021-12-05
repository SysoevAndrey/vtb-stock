from abc import ABCMeta, abstractmethod
from typing import Iterable, Optional
from uuid import UUID

from rental.core.domain.rental import Rental, RentalStatus


class RentalRepository(metaclass=ABCMeta):
    @abstractmethod
    async def filter_by_user_id(self, user_id: str) -> Iterable[Rental]:
        pass

    @abstractmethod
    async def save_rental(self, rental: Rental) -> None:
        pass

    @abstractmethod
    async def get_rental_by_user(self, rental_id: UUID, user_id: str) -> Optional[Rental]:
        pass

    @abstractmethod
    async def update_rental(self, rental: Rental) -> None:
        pass
