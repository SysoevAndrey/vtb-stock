from typing import Iterable

import inject
from gateway.core.domain.car import CarsResult
from gateway.infrastructure.gateways.cars_adapter import CarsAdapter


class CarProxyService:
    @inject.autoparams()
    def __init__(self, cars_adapter: CarsAdapter):
        self._cars = cars_adapter

    async def list_of_cars(self, page: int, size: int, show_all: bool) -> CarsResult:
        return await self._cars.list_of_cars(page, size, show_all)
