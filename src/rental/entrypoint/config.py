import os
from typing import Any, Dict, Optional


class Config:
    @property
    def is_debug(self) -> bool:
        return False

    @property
    def database_schema(self) -> Optional[str]:
        return os.getenv("DATABASE_SCHEMA")

    @property
    def database_host(self) -> str:
        return os.getenv("POSTGRES_HOST", "postgres")

    @property
    def database_port(self) -> int:
        return int(os.getenv("POSTGRES_PORT", "5432"))

    @property
    def database_name(self) -> str:
        return os.getenv("POSTGRES_DB", "services")

    @property
    def database_user(self) -> str:
        return os.getenv("POSTGRES_USER", "program")

    @property
    def database_password(self) -> Optional[str]:
        return os.getenv("POSTGRES_PASSWORD", "test")

    @property
    def database_connect_pool_size(self) -> int:
        return int(os.getenv("POSTGRES_POOL_SIZE", "10"))

    @property
    def database_connect_pool_recycle(self) -> int:
        return int(os.getenv("PG_POOL_RECYCLE", "3600"))

    @property
    def database_url(self) -> str:
        template = (
            f"postgresql+asyncpg://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )
        return template

    def to_dict(self) -> Dict[str, Any]:
        return {
            attr: getattr(self, attr) for attr in dir(self) if isinstance(getattr(type(self), attr, None), property)
        }
