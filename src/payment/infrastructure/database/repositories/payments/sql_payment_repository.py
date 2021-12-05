from typing import Optional
from uuid import UUID

from payment.core.domain.payment import Payment
from payment.core.domain.payment_repository import PaymentRepository
from shared_kernel.database.sqlalchemy_mixin import SQLAlchemyMixin
from sqlalchemy import select


class PostgreSQLPaymentRepository(PaymentRepository, SQLAlchemyMixin):
    async def save_payment(self, payment: Payment):
        self.session.add(payment)  # type: ignore

    async def update_payment(self, payment: Payment):
        await self.session.merge(payment)

    async def get_payment_by_id(self, payment_id: UUID) -> Optional[Payment]:
        filter_query = select(Payment).where(Payment.identifier == payment_id)  # type: ignore
        payment_result = await self.session.execute(filter_query)
        return payment_result.scalar()
