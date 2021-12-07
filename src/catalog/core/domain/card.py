from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Card:
    id: UUID
    image: str
    price: int
    label: str
    rating: float
    reviews_count: int
    path: str
