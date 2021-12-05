import os
from typing import Any, Dict, Optional


class Config:
    @property
    def is_debug(self) -> bool:
        return False

    @property
    def payments_host(self) -> str:
        return os.getenv("PAYMENTS_HOST", "http://localhost:8001")

    @property
    def rentals_host(self) -> str:
        return os.getenv("RENTALS_HOST", "http://localhost:8002")

    @property
    def cars_host(self) -> str:
        return os.getenv("CARS_HOST", "http://localhost:8003")

    def to_dict(self) -> Dict[str, Any]:
        return {
            attr: getattr(self, attr) for attr in dir(self) if isinstance(getattr(type(self), attr, None), property)
        }
