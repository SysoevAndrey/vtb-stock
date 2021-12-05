from typing import Iterable, Optional, Tuple
from uuid import UUID

from stock.core.domain import Car, CarRepository
from shared_kernel.database.sqlalchemy_mixin import SQLAlchemyMixin
from sqlalchemy import func, select


class PostgreSQLCarRepository(CarRepository, SQLAlchemyMixin):
    async def create_tables(self):
        conn = await self.session.connection()
        await conn.run_sync(self.metadata.create_all)  # type: ignore

    async def list(self, skip: int, limit: int) -> Tuple[Iterable[Car], int]:
        query = select(Car).limit(limit).offset(skip)  # type: ignore
        cars = await self.session.execute(query)
        count = await self.session.execute(select(func.count(Car.identifier)))
        return list(cars.scalars()), count.scalar()

    async def filter_cars_by_availability(self, skip: int, limit: int, availability: bool) -> Tuple[Iterable[Car], int]:
        filter_query = select(Car).where(Car.available == availability)  # type: ignore
        pagination_query = filter_query.limit(limit).offset(skip)
        cars = await self.session.execute(pagination_query)
        count = await self.session.execute(select(func.count()).where(Car.available == availability))
        return list(cars.scalars()), count.scalar()

    async def save(self, car: Car):
        self.session.add(car)  # type: ignore

    async def get_car_by_id(self, identifier: UUID, available: bool | str = True) -> Optional[Car]:
        if isinstance(available, bool):
            filter_query = select(Car).where(Car.identifier == identifier).where(Car.available == available)  # type: ignore
        else:
            filter_query = select(Car).where(Car.identifier == identifier)  # type: ignore
        car = await self.session.execute(filter_query)
        return car.scalar()

    async def update_car(self, car: Car):
        await self.session.merge(car)
