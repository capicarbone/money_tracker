from uuid import uuid4
from datetime import date, datetime
from typing import List, Generic, TypeVar
from pydantic import BaseModel
from sqlalchemy import create_engine, Engine, delete, select
from sqlalchemy.orm import Session
from money_tracker.managers import accounts
from money_tracker.models import *
from money_tracker.daos.base import (
    AbsTransactionCategoryDAO,
    DataAccessObject,
    AbsTransactionsDAO,
    AbsAccountsDAO,
)
from money_tracker.daos.sql_generic.models import (
    MappedAccount,
    MappedCategory,
    MappedTransaction,
)
from money_tracker.models import Account, Transaction

T = TypeVar("T")
S = TypeVar("S")


class BaseSQLEntityDAO(Generic[T, S]):
    model_class = None
    engine: Engine = None

    def __init__(self, engine: Engine) -> None:
        self.engine: Engine = engine

        if self.model_class is None:
            raise Exception("model_class attribute is missing.")

    def save(self, entity: S) -> S:
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

    def get(self, entity_id: str) -> BaseModel:
        with Session(self.engine) as session:
            return session.get(self.model_class, entity_id).to_object()


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
    AbsTransactionCategoryDAO,
):
    model_class = MappedCategory

    def delete(self, entity: BaseModel):
        # Validate no related transactions
        return super().delete(entity)


class GenericSQLTransactionDAO(
    BaseSQLEntityDAO[MappedTransaction, Transaction], AbsTransactionsDAO
):
    model_class = MappedTransaction

    def save(self, entity: Transaction) -> Transaction:
        # entity.creation_date = datetime.today()
        # return super().save(entity)

        raise Exception("Use save_group instead.")

    def save_group(self, transactions: List[Transaction]):
        creation_time = datetime.today()
        group_id = str(uuid4())

        with Session(self.engine) as session:
            rows = {}
            for t in transactions:
                t.creation_date = creation_time
                if len(transactions) > 1:
                    t.group_id = group_id
                row = self.model_class(**t.model_dump())
                session.add(row)
                rows[row] = t

                account: MappedAccount = session.get(MappedAccount, t.account_id)
                account.balance += t.change

            session.commit()

            for row in rows.keys():
                rows[row].id = row.id

        return transactions

    def delete(self, transaction: Transaction):
        with Session(self.engine) as session:
            if transaction.group_id:
                stmt = select(MappedTransaction).where(
                    MappedTransaction.group_id == transaction.group_id
                )
                result = session.execute(stmt).scalars()
                for row in result:
                    session.delete(row)
            else:
                db_obj = session.get(MappedTransaction, transaction.id)
                session.delete(db_obj)

            session.commit()

    def filter(
        self,
        account_id: str = None,
        start_date: date = None,
        end_date: date = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Transaction]:
        with Session(self.engine) as session:
            stmt = select(MappedTransaction)

            if start_date and end_date:
                if end_date < start_date:
                    raise Exception("start_date must be before end_date")

            if account_id:
                stmt = stmt.where(MappedTransaction.account_id == account_id)

            if start_date:
                stmt = stmt.where(MappedTransaction.execution_date >= start_date)

            if end_date:
                stmt = stmt.where(MappedTransaction.execution_date <= end_date)

            stmt = stmt.limit(limit).offset(offset).order_by(MappedTransaction.execution_date.desc() )

            result = session.execute(stmt).scalars()

            transactions = [r.to_object() for r in result]

            return transactions
