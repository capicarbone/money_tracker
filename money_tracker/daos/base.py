from typing import List
from datetime import date
from pydantic import BaseModel

from money_tracker.models import Account, Transaction, Category

# Exceptions

# Abstract classes


class DataAccessObject:
    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError()

    def save(self, entity: BaseModel) -> BaseModel:
        raise NotImplementedError()

    def delete(self, entity: BaseModel):
        raise NotImplementedError()

    def update(self, entity: BaseModel):
        raise NotImplementedError()

    def get(self, entity_id: str) -> BaseModel:
        raise NotImplementedError()


class AbsTransactionsDAO(DataAccessObject):
    def filter(
        self, account_id: str, start_date: date, end_date: date, limit: int, offset: int
    ) -> List[Transaction]:
        raise NotImplementedError()

    def save_group(self, transactions: List[Transaction]):
        raise NotImplementedError()


class AbsAccountsDAO(DataAccessObject):
    def get_all(self) -> List[Account]:
        raise NotImplementedError()


class AbsTransactionCategoryDAO(DataAccessObject):
    def get_all(self) -> List[Category]:
        raise NotImplementedError()

class AbsDAOFactory():

    def __init__(self) -> None:
        self.transaction_dao: AbsTransactionsDAO = None
        self.category_dao: AbsTransactionCategoryDAO = None
        self.account_dao: AbsAccountsDAO = None

    def _create_transaction_dao(self) -> AbsTransactionsDAO:
        raise NotImplementedError()

    def get_transaction_dao(self) -> AbsTransactionsDAO:
        if not self.transaction_dao:
            self.transaction_dao = self._create_transaction_dao()

        return self.transaction_dao
    
    def _create_category_dao(self) -> AbsTransactionCategoryDAO:
        raise NotImplementedError()
    
    def get_category_dao(self) -> AbsTransactionCategoryDAO:
        if not self.category_dao:
            self.category_dao = self._create_category_dao()

        return self.category_dao
    
    def _create_account_dao(self) -> AbsAccountsDAO:
        raise NotImplementedError()
    
    def get_account_dao(self) -> AbsAccountsDAO:
        if not self.account_dao:
            self.account_dao = self._create_account_dao()

        return self.account_dao
        