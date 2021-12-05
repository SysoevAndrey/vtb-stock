import inject
from shared_kernel.database.connectors import SQLAlchemyDatabaseConnector
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.schema import MetaData


class SQLAlchemyMixin:
    @inject.autoparams()  # TODO: подумать над расположением этого класса
    def __init__(self, db_connector: SQLAlchemyDatabaseConnector):
        self._db_connector = db_connector

    @property
    def metadata(self) -> MetaData:
        return self._db_connector.metadata

    @property
    def session(self) -> AsyncSession:
        return self._db_connector.get_current_session()
