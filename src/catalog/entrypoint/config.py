import os
from typing import Any, Dict, Optional


class Config:
    @property
    def is_debug(self) -> bool:
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            attr: getattr(self, attr) for attr in dir(self) if isinstance(getattr(type(self), attr, None), property)
        }
