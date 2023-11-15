from typing import List
from uuid import uuid4
from decimal import Decimal
from datetime import datetime, date

from money_tracker.models import (
    Transaction,
    INCOME_TRANSACTION_TYPE,
    EXPENSE_TRANSACTION_TYPE,
    TRANSFER_IN_TRANSACTION_TYPE,
    TRANSFER_OUT_TRANSACTION_TYPE,
)
from money_tracker.daos.base import (
    AbsAccountsDAO,
    AbsTransactionsDAO,
    AbsTransactionCategoriesDAO,
)


class TransactionsManager:
    accounts_dao: AbsAccountsDAO
    transactions_dao: AbsTransactionsDAO
    categories_dao: AbsTransactionCategoriesDAO

    def __init__(
        self,
        accounts_dao: AbsAccountsDAO,
        transactions_dao: AbsTransactionsDAO,
        categories_dao: AbsTransactionCategoriesDAO,
    ) -> None:
        self.accounts_dao = accounts_dao
        self.transactions_dao = transactions_dao
        self.categories_dao = categories_dao

    def __add_transactions(self, transactions: List[Transaction]) -> List[Transaction]:
        for t in transactions:
            if not self.accounts_dao.exists(t.account_id):
                raise Exception("Invalid account id")  # TODO create dedicated exception
            elif t.transaction_type not in [
                TRANSFER_IN_TRANSACTION_TYPE,
                TRANSFER_OUT_TRANSACTION_TYPE,
            ] and not self.categories_dao.exists(t.category_id):
                raise Exception(
                    "Invalid category id"
                )  # TODO create dedicated exception

        self.transactions_dao.save_group(transactions)

        return transactions

    def add_income(
        # self, change: Decimal, execution_date: date, account_id: str, category_id: str, description: str
        self,
        **kwargs
    ) -> Transaction:
        kwargs["transaction_type"] = INCOME_TRANSACTION_TYPE
        kwargs["creation_date"] = date.today()
        transactions = self.__add_transactions([Transaction(**kwargs)])

        return transactions[0]

    def add_expense(self, **kwargs) -> Transaction:
        kwargs["transaction_type"] = EXPENSE_TRANSACTION_TYPE
        kwargs["creation_date"] = date.today()
        transactions = self.__add_transactions([Transaction(**kwargs)])

        return transactions[0]

    def add_transfer(
        self,
        change: Decimal,
        from_account_id: str,
        to_account_id: str,
        execution_date: date,
        description: str = None,
    ) -> (Transaction, Transaction):
        group_id = str(uuid4())
        creation_date = date.today()

        transfer_in = Transaction(
            change=change,
            transaction_type=TRANSFER_IN_TRANSACTION_TYPE,
            account_id=to_account_id,
            execution_date=execution_date,
            description=description,
            creation_date=creation_date,
            group_id=group_id,
        )

        transfer_out = Transaction(
            change=-change,
            transaction_type=TRANSFER_OUT_TRANSACTION_TYPE,
            account_id=from_account_id,
            execution_date=execution_date,
            description=description,
            creation_date=creation_date,
            group_id=group_id,
        )

        self.__add_transactions([transfer_in, transfer_out])

        return transfer_in, transfer_out

    def remove_transaction(self, transaction_id: str):
        self.transactions_dao.delete(transaction_id)

    def update_transaction(
        self,
        transaction_id: str,
        change: Decimal = None,
        account_id: str = None,
        category_id: str = None,
        execution_time: date = None,
    ):
        transaction: Transaction = self.transactions_dao.get(transaction_id)

        if change:
            transaction.change = change

        if account_id:
            transaction.account_id = account_id

        self.transactions_dao.update(transaction)

    def get_transactions(
        self,
        account_id: str = None,
        start_date: date = None,
        end_date: str = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Transaction]:
        return self.transactions_dao.get_transactions(
            account_id=account_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset,
        )

    def move_transaction(self, transaction_id: str, account_id: str):
        self.update_transaction(transaction_id=transaction_id, account_id=account_id)
