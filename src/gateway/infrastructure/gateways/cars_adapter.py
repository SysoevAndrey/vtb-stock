from typing import Iterable
from uuid import UUID
from gateway.core.domain.car import Car, CarsResult
from gateway.infrastructure.gateways.loaders.car_schema import CarLoaderSchema, CarResultLoaderSchema
import aiohttp


class CarsAdapter:
    cars_schema = CarResultLoaderSchema()
    car_single_schema = CarLoaderSchema()

    def __init__(self, host: str):
        self._host = host
        self._cars_url = f"{host}/api/cars"

    async def list_of_cars(self, page: int, size: int, show_all: bool) -> CarsResult:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self._cars_url}", params={"page": page, "size": size, "showAll": str(show_all)}
            ) as resp:
                resp.raise_for_status()
                return self.cars_schema.load(await resp.json())

    async def get_car_by_id(self, car_id: UUID) -> Car:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._cars_url}/{car_id}") as resp:
                resp.raise_for_status()
                return self.car_single_schema.load(await resp.json())

    async def reserve_car(self, car_id: UUID):
        async with aiohttp.ClientSession() as session:
            async with session.patch(f"{self._cars_url}/{car_id}/reserve") as resp:
                resp.raise_for_status()
                await resp.read()

    async def free_car(self, car_id: UUID):
        async with aiohttp.ClientSession() as session:
            async with session.patch(f"{self._cars_url}/{car_id}/free") as resp:
                resp.raise_for_status()
                await resp.read()
