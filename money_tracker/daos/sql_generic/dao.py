from os import name
from typing import List, Generic, TypeVar
from pydantic import BaseModel
from sqlalchemy import create_engine, Engine, select
from sqlalchemy.orm import Session
from money_tracker.managers import accounts
from money_tracker.models import *
from money_tracker.daos.base import AbsTransactionCategoriesDAO, DataAccessObject, AbsTransactionsDAO, AbsAccountsDAO
from money_tracker.daos.sql_generic.models import MappedAccount, MappedCategory
from money_tracker.models import Account

T = TypeVar("T")
S = TypeVar("S")


class BaseSQLEntityDAO(Generic[T, S]):
    model_class = None
    engine: Engine = None

    def __init__(self, engine: Engine) -> None:
        self.engine: Engine = engine

        if self.model_class is None:
            raise Exception("model_class attribute is missing.")

    def save(self, entity: T) -> S:
        with Session(self.engine) as session:
            row = self.model_class(**entity.model_dump())
            session.add(row)
            session.commit()

            entity.id = row.id

        return entity

    def exists(self, entity_id: str) -> bool:
        with Session(self.engine) as session:
            result = session.get(self.model_class, entity_id)

            return result is not None


class SQLGetAllImplementationMixin(Generic[S]):
    def get_all(self) -> List[S]:
        stmt = select(self.model_class)
        with Session(self.engine) as session:
            results = session.execute(stmt).scalars()

            accounts = [row.to_object() for row in results]

        return accounts


class GenericSQLAccountDAO(
    BaseSQLEntityDAO[MappedAccount, Account],
    SQLGetAllImplementationMixin[Account],
    AbsAccountsDAO,
):
    model_class = MappedAccount

    def delete(self, entity: BaseModel):
        # Validate no related transactions
        return super().delete(entity)


class GenericSQLCategoryDAO(
    BaseSQLEntityDAO[MappedCategory, Category],
    SQLGetAllImplementationMixin[Category],
    AbsTransactionCategoriesDAO
):
    model_class = MappedCategory

    def delete(self, entity: BaseModel):
        # Validate no related transactions
        return super().delete(entity)