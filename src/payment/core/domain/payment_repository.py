from abc import ABCMeta, abstractmethod
from typing import Optional
from uuid import UUID

from payment.core.domain.payment import Payment


class PaymentRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save_payment(self, payment: Payment):
        pass

    @abstractmethod
    async def update_payment(self, payment: Payment):
        pass

    @abstractmethod
    async def get_payment_by_id(self, payment_id: UUID) -> Optional[Payment]:
        pass
