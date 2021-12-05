from typing import Iterable
from uuid import UUID

import aiohttp
from gateway.application.request_mapper.create_rental_request import CreateRentalRequest
from gateway.infrastructure.gateways.loaders.rental_schema import RentalProjection, RentalProjectionSchema
from loguru import logger


class RentalsAdapter:
    rentals_schema = RentalProjectionSchema()

    def __init__(self, host: str):
        self._host = host
        self._rentals_url = f"{self._host}/api/rental"

    async def get_all_rentals_for_user(self, user_id: str) -> Iterable[RentalProjection]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._rentals_url}", headers={"X-User-Name": user_id}) as resp:
                resp.raise_for_status()
                rentals = await resp.json()
                return [self.rentals_schema.load(rental) for rental in rentals]

    async def get_rental_for_user(self, user_id: str, rental_id: UUID) -> RentalProjection:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._rentals_url}/{rental_id}", headers={"X-User-Name": user_id}) as resp:
                resp.raise_for_status()
                return self.rentals_schema.load(await resp.json())

    async def finish(self, user_id: str, rental_id: UUID):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self._rentals_url}/{rental_id}/finish", headers={"X-User-Name": user_id}
            ) as resp:
                resp.raise_for_status()
                await resp.read()

    async def cancel(self, user_id: str, rental_id: UUID):
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{self._rentals_url}/{rental_id}", headers={"X-User-Name": user_id}) as resp:
                resp.raise_for_status()
                await resp.read()

    async def rent_car(
        self, rental_request: CreateRentalRequest, car_id: UUID, payment_uid: UUID, user_id: str
    ) -> RentalProjection:
        async with aiohttp.ClientSession() as session:
            json_data = {
                "carUid": str(car_id),
                "paymentUid": str(payment_uid),
                "dateFrom": str(rental_request.date_from),
                "dateTo": str(rental_request.date_to),
            }
            logger.debug(f"Rental request data: {json_data}")
            async with session.post(
                f"{self._rentals_url}",
                headers={"X-User-Name": user_id},
                json=json_data,
            ) as resp:
                data = await resp.json()
                resp.raise_for_status()
                return self.rentals_schema.load(data)
