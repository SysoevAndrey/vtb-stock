import uuid
from typing import Iterable, Optional

import inject
from loguru import logger
from rental.application.request_mapper.create_rental_request import CreateRentalRequest
from rental.core.domain.rental import Rental, RentalStatus
from rental.core.domain.rental_repository import RentalRepository
from shared_kernel.database.transaction import async_transactional


class RentalListService:
    @inject.autoparams()
    def __init__(self, rental_repo: RentalRepository):
        self._rental_repo = rental_repo

    @async_transactional
    async def show_rentals_for_user(self, user_id: str) -> Iterable[Rental]:
        return await self._rental_repo.filter_by_user_id(user_id)

    @async_transactional
    async def save_rental_for_user(self, rental_request: CreateRentalRequest, user_id: str) -> Rental:
        rental = Rental(
            identifier=uuid.uuid4(),
            user_id=user_id,
            date_from=rental_request.date_from,
            date_to=rental_request.date_to,
            car_uid=rental_request.car_uid,
            payment_uid=rental_request.payment_uid,
        )
        await self._rental_repo.save_rental(rental)
        return rental

    @async_transactional
    async def show_rental_for_user(self, user_id: str, rental_id: uuid.UUID) -> Optional[Rental]:
        return await self._rental_repo.get_rental_by_user(rental_id=rental_id, user_id=user_id)

    @async_transactional
    async def decline_rental_for_user(self, user_id: str, rental_uid: uuid.UUID) -> Optional[Rental]:
        return await self._change_rental_status(user_id=user_id, rental_uid=rental_uid, status=RentalStatus.CANCELED)

    @async_transactional
    async def finish_rental_for_user(self, user_id: str, rental_uid: uuid.UUID) -> Optional[Rental]:
        return await self._change_rental_status(user_id=user_id, rental_uid=rental_uid, status=RentalStatus.FINISHED)

    @async_transactional
    async def start_rental_for_user(self, user_id: str, rental_uid: uuid.UUID) -> Optional[Rental]:
        return await self._change_rental_status(user_id=user_id, rental_uid=rental_uid, status=RentalStatus.IN_PROGRESS)

    async def _change_rental_status(
        self, user_id: str, rental_uid: uuid.UUID, status: RentalStatus
    ) -> Optional[Rental]:
        rental = await self._rental_repo.get_rental_by_user(rental_id=rental_uid, user_id=user_id)
        if not rental:
            logger.info(
                f"Rental - {rental_uid} for user - '{user_id}' was not found. Change operation was not permitted."
            )
            return rental

        changed_rental = rental.set_status(status)

        if changed_rental.status is not rental.status:
            await self._rental_repo.update_rental(changed_rental)
            return changed_rental
        return None
