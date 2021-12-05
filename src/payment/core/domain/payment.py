from dataclasses import dataclass, replace
from enum import Enum
from uuid import UUID

from loguru import logger


class PaymentStatus(Enum):
    PAID = "PAID"
    CANCELED = "CANCELED"


@dataclass
class Payment:
    identifier: UUID
    price: int
    status: PaymentStatus = PaymentStatus.PAID

    def decline(self) -> "Payment":
        if self.status == PaymentStatus.CANCELED:
            logger.warning(f"Payment '{self.identifier}' already declined. Decline operation was not permitted.")
            return self
        return replace(self, status=PaymentStatus.CANCELED)
