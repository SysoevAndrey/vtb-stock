import uuid
from typing import Optional

import inject
from cars.application.request_mapper.create_car_request import CreateCarRequest
from cars.core.domain import Car, CarRepository
from cars.core.domain.cars_result import CarsResult
from loguru import logger
from shared_kernel.database.transaction import async_transactional


class CarListService:
    @inject.autoparams()
    def __init__(self, car_repository: CarRepository):
        self._cars = car_repository

    @async_transactional
    async def get_car_by_id(self, car_id: uuid.UUID) -> Optional[Car]:
        return await self._cars.get_car_by_id(car_id, available="all")

    @async_transactional
    async def show_cars(self, page: int, size: int, show_all: bool) -> CarsResult:
        skip = (page - 1) * size

        if show_all:
            cars, count = await self._cars.list(skip=skip, limit=size)
        else:
            cars, count = await self._cars.filter_cars_by_availability(skip=skip, limit=size, availability=True)

        return CarsResult(total_count=count, cars=list(cars))

    @async_transactional
    async def save_car(self, car_request: CreateCarRequest):
        car = Car(identifier=uuid.uuid4(), **car_request.dict(by_alias=False))
        await self._cars.save(car)
        return car

    @async_transactional
    async def reserve_car(self, car_uid: uuid.UUID) -> Optional[Car]:
        car = await self._cars.get_car_by_id(car_uid, available="all")

        if car:
            reserved_car = car.reserve()
            if reserved_car.available == car.available:
                return None
            await self._cars.update_car(reserved_car)
        else:
            logger.info(f"Car '{car_uid}' was not found. Reserve operation was not permitted.")

        return car

    @async_transactional
    async def free_car(self, car_uid: uuid.UUID) -> Optional[Car]:
        car = await self._cars.get_car_by_id(car_uid, available="all")

        if car:
            free_car = car.free()
            if free_car.available == car.available:
                return None
            await self._cars.update_car(free_car)
        else:
            logger.info(f"Car '{car_uid}' was not found. Free operation was not permitted.")

        return car
