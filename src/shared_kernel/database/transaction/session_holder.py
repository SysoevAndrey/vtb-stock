import inspect
import logging
from contextvars import ContextVar
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession


logger = logging.getLogger(__name__)


class NoCurrentSession(Exception):
    pass


class SessionHolder:
    session: ContextVar[Optional[AsyncSession]] = ContextVar("session", default=None)

    @staticmethod
    def get_session() -> AsyncSession:
        current_session = SessionHolder.session.get()
        if not current_session:
            func = inspect.stack()[4]
            raise NoCurrentSession(str(func))
        else:
            return current_session

    @staticmethod
    def set_session(session):
        SessionHolder.session.set(session)

    @staticmethod
    def detach_session() -> None:
        SessionHolder.session.set(None)
