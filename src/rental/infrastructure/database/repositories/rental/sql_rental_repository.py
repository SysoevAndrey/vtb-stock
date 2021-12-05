from typing import Iterable, Optional
from uuid import UUID

from rental.core.domain.rental import Rental
from rental.core.domain.rental_repository import RentalRepository
from shared_kernel.database.sqlalchemy_mixin import SQLAlchemyMixin
from sqlalchemy import select


class PostgreSQLRentalRepository(RentalRepository, SQLAlchemyMixin):
    async def filter_by_user_id(self, user_id: str) -> Iterable[Rental]:
        query = select(Rental).where(Rental.user_id == user_id)  # type: ignore
        rentals = await self.session.execute(query)
        return rentals.scalars()

    async def get_rental_by_user(self, rental_id: UUID, user_id: str) -> Optional[Rental]:
        filter_query = select(Rental).where(Rental.identifier == rental_id).where(Rental.user_id == user_id)  # type: ignore
        rental = await self.session.execute(filter_query)
        return rental.scalar()

    async def save_rental(self, rental: Rental) -> None:
        self.session.add(rental)  # type: ignore

    async def update_rental(self, rental: Rental) -> None:
        await self.session.merge(rental)
