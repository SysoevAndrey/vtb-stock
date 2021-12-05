from typing import Iterable, Tuple
from uuid import UUID

import inject
from gateway.application.request_mapper.create_rental_request import CreateRentalRequest
from gateway.core.domain.payment import Payment
from gateway.core.domain.rental import Rental
from gateway.infrastructure.gateways.cars_adapter import CarsAdapter
from gateway.infrastructure.gateways.loaders.rental_schema import RentalProjection
from gateway.infrastructure.gateways.payments_adapter import PaymentsAdapter
from gateway.infrastructure.gateways.rentals_adapter import RentalsAdapter
from loguru import logger


class RentalProxyService:
    @inject.autoparams()
    def __init__(self, cars_adapter: CarsAdapter, rentals_adapter: RentalsAdapter, payments_adapter: PaymentsAdapter):
        self._cars = cars_adapter
        self._rentals = rentals_adapter
        self._payments = payments_adapter

    async def get_assembled_rentals(self, user_id: str) -> Iterable[Rental]:
        rentals = await self._rentals.get_all_rentals_for_user(user_id)

        return [
            Rental(
                identifier=rental.identifier,
                status=rental.status,
                date_from=rental.date_from,
                date_to=rental.date_to,
                car=await self._cars.get_car_by_id(rental.car_uid),
                payment=await self._payments.get_payment_by_id(rental.payment_uid),
            )
            for rental in rentals
        ]

    async def get_assembled_rental(self, user_id: str, rental_uid: UUID) -> Rental:
        rental = await self._rentals.get_rental_for_user(user_id, rental_uid)

        return Rental(
            identifier=rental.identifier,
            status=rental.status,
            date_from=rental.date_from,
            date_to=rental.date_to,
            car=await self._cars.get_car_by_id(rental.car_uid),
            payment=await self._payments.get_payment_by_id(rental.payment_uid),
        )

    async def apply_rental(self, user_id: str, rental_request: CreateRentalRequest) -> Tuple[RentalProjection, Payment]:
        car = await self._cars.get_car_by_id(rental_request.car_uid)
        if not car:
            logger.error(f"Car '{rental_request.car_uid}' for user {user_id} was not found.")
            raise RuntimeError("Car with requested identifier was not found.")

        await self._cars.reserve_car(rental_request.car_uid)

        total_price = car.price * int((rental_request.date_to - rental_request.date_from).days)

        payment_info = await self._payments.save_payment_info(total_price)

        rental = await self._rentals.rent_car(rental_request, car.identifier, payment_info.identifier, user_id)

        return (rental, payment_info)

    async def finish_rental(self, user_id: str, rental_id: UUID):
        rental = await self._rentals.get_rental_for_user(user_id, rental_id=rental_id)

        await self._cars.free_car(rental.car_uid)
        await self._rentals.finish(user_id, rental_id=rental_id)

    async def cancel_rental(self, user_id: str, rental_id: UUID):
        rental = await self._rentals.get_rental_for_user(user_id, rental_id=rental_id)

        await self._cars.free_car(rental.car_uid)
        await self._payments.decline_payment(rental.payment_uid)
        await self._rentals.cancel(user_id, rental_id)
