import logging
from typing import Any, Callable

import inject
from shared_kernel.database.transaction.manager import DatabaseTransactionManager

logger = logging.getLogger(__name__)


@inject.autoparams()
def async_transactional(func: Callable[..., Any]) -> Callable[..., Any]:
    async def transactional_wrapper(*args, **kwargs):
        tm = inject.instance(DatabaseTransactionManager)
        exception = None
        result = None
        transaction = tm.get_transaction()

        try:
            result = await func(*args, **kwargs)
        except Exception as e:
            exception = e
            logger.error(f"Transaction {transaction.id} will be rolled back. Reason: {exception}.")

        if exception:
            try:
                await tm.rollback(transaction)
            except Exception as e:
                logger.error(f"Transaction {transaction.id} could not rollback. Reason: {e}.")
            raise exception
        else:
            await tm.commit(transaction)
        return result

    return transactional_wrapper


__all__ = ["async_transactional"]
