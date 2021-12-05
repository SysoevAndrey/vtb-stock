from asyncio import current_task
from typing import Optional

from shared_kernel.database.connectors.base_connector import SQLAlchemyDatabaseConnector
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.pool import NullPool
from loguru import logger


class PostgreSQLConnector(SQLAlchemyDatabaseConnector):
    def __init__(
        self,
        database_url: str,
        database_connect_pool_size: int,
        database_connect_pool_recycle: int,
        schema: Optional[str] = None,
    ):
        self._engine = create_async_engine(
            database_url,
            pool_pre_ping=True,
            pool_recycle=database_connect_pool_recycle,
            max_overflow=5,
            pool_size=database_connect_pool_size,
        )
        logger.debug(f"Engine created - {self._engine}")
        session_factory_type = async_scoped_session(  # thread-safety
            sessionmaker(
                bind=self.engine,
                expire_on_commit=False,
                class_=AsyncSession,
            ),
            current_task,
        )
        self._session_maker = session_factory_type
        if schema:
            self._metadata = MetaData(schema=schema)
        else:
            self._metadata = MetaData(schema=schema)
        super().__init__(schema=schema)

    @property
    def metadata(self) -> MetaData:
        return self._metadata

    @property
    def session_maker(self) -> async_scoped_session:
        return self._session_maker

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    def ping(self):
        self.engine.sync_engine.execute("SELECT 1")

    async def repair_after_fork(self):
        await self.engine.dispose()
