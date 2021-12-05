import inspect
import logging
from contextvars import ContextVar

import uuid

logger = logging.getLogger(__name__)


class Transaction:
    id: int
    is_new: bool
    is_failed = ContextVar("is_failed", default=False)

    def __init__(self, is_new: bool):
        self.id = uuid.uuid4().int
        self.is_new = is_new
        func = inspect.stack()[4]
        logger.info(
            f"TX {self.id} started. Is new: {self.is_new}. "
            f"Function: {func.function}. File: {func.filename}. Line: {func.lineno}."
        )

    @property
    def need_rollback(self):
        return bool(self.is_failed.get())
