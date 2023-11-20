from sqlalchemy import Engine, create_engine
from money_tracker.daos.base import (
    AbsAccountsDAO,
    AbsDAOFactory,
    AbsTransactionCategoryDAO,
    AbsTransactionsDAO,
)
from money_tracker.daos.sql_generic.dao import (
    GenericSQLAccountDAO,
    GenericSQLCategoryDAO,
    GenericSQLTransactionDAO,
)


class SQLiteDAOFactory(AbsDAOFactory):
    engine: Engine = None

    def __init__(self, file_path) -> None:
        self.engine = create_engine(f"sqlite+pysqlite:///{file_path}")

    def _create_account_dao(self) -> AbsAccountsDAO:
        return GenericSQLAccountDAO(self.engine)

    def _create_category_dao(self) -> AbsTransactionCategoryDAO:
        return GenericSQLCategoryDAO(self.engine)

    def _create_transaction_dao(self) -> AbsTransactionsDAO:
        return GenericSQLTransactionDAO(self.engine)
