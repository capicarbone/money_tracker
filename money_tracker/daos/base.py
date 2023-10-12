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
    def get_transactions(
        self, account_id: str, start_date: date, end_date: date, limit: int, offset: int
    ) -> List[Transaction]:
        raise NotImplementedError()

    def save_many(self, transactions: List[Transaction]):
        raise NotImplementedError()


class AbsAccountsDAO(DataAccessObject):
    def get_all(self) -> List[Account]:
        raise NotImplementedError()


class AbsTransactionCategoriesDAO(DataAccessObject):
    def get_all(self) -> List[Category]:
        raise NotImplementedError()
