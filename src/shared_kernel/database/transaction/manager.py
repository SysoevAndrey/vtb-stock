import inject
from shared_kernel.database.connectors import SQLAlchemyDatabaseConnector
from shared_kernel.database.transaction.session_holder import SessionHolder
from shared_kernel.database.transaction.transaction import Transaction
from loguru import logger


class DatabaseTransactionManager:
    @inject.autoparams()
    def __init__(self, db: SQLAlchemyDatabaseConnector):
        self._db = db

    def get_transaction(self):
        current_session = SessionHolder.session.get()
        if current_session:
            transaction = Transaction(is_new=False)
        else:
            transaction = Transaction(is_new=True)
            session = self._db.session_maker()
            SessionHolder.set_session(session)
        return transaction

    async def commit(self, transaction: Transaction):
        if transaction.is_new:
            session = SessionHolder.get_session()
            try:
                await session.commit()
            except Exception as commit_error:
                try:
                    await session.rollback()
                except Exception as rollback_error:
                    logger.error(f"Transaction {transaction.id} could not rollback session. Reason: {rollback_error}.")
                raise commit_error
            finally:
                SessionHolder.detach_session()
                try:
                    await session.close()
                    logger.info(f"Transaction {transaction.id} closed.")
                except Exception as e:
                    logger.warning(f"Transaction {transaction.id} could not close session. Reason: {e}.")
        else:
            logger.info(f"Transaction {transaction.id} will be committed.")

    async def rollback(self, transaction: Transaction):
        if transaction.is_new:
            session = SessionHolder.get_session()
            SessionHolder.detach_session()
            try:
                await session.rollback()
                logger.warning(f"Transaction {transaction.id} rolled back.")
            except Exception as e:
                logger.warning(f"Transaction {transaction.id}. Error on rollback: {e}.")
                raise e
            finally:
                try:
                    await session.close()
                except Exception as e:
                    logger.warning(f"Transaction {transaction.id}. Error on closing: {e}.")
        else:
            transaction.is_failed.set(True)
            logger.warning(f"Transaction {transaction.id} will be rolled back.")
