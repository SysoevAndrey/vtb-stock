import uuid
from typing import Optional

import inject
from loguru import logger
from payment.application.request_mapper.create_payment_request import CreatePaymentRequest
from payment.core.domain.payment import Payment
from payment.core.domain.payment_repository import PaymentRepository
from shared_kernel.database.transaction import async_transactional


class PaymentListService:
    @inject.autoparams()
    def __init__(self, payment_repo: PaymentRepository):
        self._payments = payment_repo

    @async_transactional
    async def get_payment_by_id(self, payment_id: uuid.UUID) -> Optional[Payment]:
        return await self._payments.get_payment_by_id(payment_id=payment_id)

    @async_transactional
    async def decline_payment(self, payment_id: uuid.UUID) -> Optional[Payment]:
        payment = await self._payments.get_payment_by_id(payment_id=payment_id)

        if not payment:
            logger.debug(f"Payment '{payment_id}' was not found. Decline operation was not permitted.")
            return None

        declined_payment = payment.decline()

        if declined_payment.status == payment.status:
            return None

        await self._payments.update_payment(declined_payment)

        return declined_payment

    @async_transactional
    async def save_payment(self, payment_request: CreatePaymentRequest) -> Payment:
        payment = Payment(identifier=uuid.uuid4(), price=payment_request.price)
        await self._payments.save_payment(payment)
        return payment
