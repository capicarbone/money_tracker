from sqlalchemy import Engine, create_engine, inspect
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
from money_tracker.daos.sql_generic.models import Base


class SQLiteDAOFactory(AbsDAOFactory):

    def __init__(self, file_path) -> None:
        super().__init__()
        self.engine = create_engine(f"sqlite+pysqlite:///{file_path}")

        if not inspect(self.engine).has_table("account"):
            Base.metadata.create_all(self.engine)

    def _create_account_dao(self) -> AbsAccountsDAO:
        return GenericSQLAccountDAO(self.engine)

    def _create_category_dao(self) -> AbsTransactionCategoryDAO:
        return GenericSQLCategoryDAO(self.engine)

    def _create_transaction_dao(self) -> AbsTransactionsDAO:
        return GenericSQLTransactionDAO(self.engine)
