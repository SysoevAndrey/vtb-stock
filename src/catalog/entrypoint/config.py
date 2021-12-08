import os
from typing import Any, Dict


class Config:
    @property
    def is_debug(self) -> bool:
        return False

    @property
    def elasticsearch_host(self) -> str:
        return os.getenv("ELASTICSEARCH_HOST", "es-vtb")

    @property
    def elasticsearch_port(self) -> int:
        return int(os.getenv("ELASTICSEARCH_PORT", "9200"))

    @property
    def elasticsearch_cards_index(self) -> str:
        return os.getenv("ELASTICSEARCH_CARDS_INDEX", "cards")

    def to_dict(self) -> Dict[str, Any]:
        return {
            attr: getattr(self, attr) for attr in dir(self) if isinstance(getattr(type(self), attr, None), property)
        }
