from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class PaymentStatus(Enum):
    PAID = "PAID"
    CANCELED = "REVERSED"


@dataclass
class Payment:
    identifier: UUID
    price: int
    status: PaymentStatus
