from abc import ABCMeta, abstractmethod
from typing import Callable, Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_scoped_session
from sqlalchemy.sql.schema import MetaData


class SQLAlchemyDatabaseConnector(metaclass=ABCMeta):
    def __init__(self, schema: Optional[str] = None):
        self.schema = schema

    def prepare_db(
        self, mapping_callbacks: Sequence[Callable[["SQLAlchemyDatabaseConnector"], None]], create_tables=False
    ):
        for callback in mapping_callbacks:
            callback(self)

        # if create_tables:
        #     self.metadata.create_all()

    def get_current_session(self) -> AsyncSession:
        """
        This function calls only under transaction!
        """
        return self.session_maker()

    async def close_current_session(self):
        await self.session_maker.remove()

    @property
    @abstractmethod
    def metadata(self) -> MetaData:
        pass

    @property
    @abstractmethod
    def session_maker(self) -> async_scoped_session:
        pass

    @property
    @abstractmethod
    def engine(self) -> AsyncEngine:
        pass

    @abstractmethod
    def ping(self):
        pass
