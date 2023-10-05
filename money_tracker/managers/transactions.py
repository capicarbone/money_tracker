from typing import List
from decimal import Decimal
from datetime import datetime, date

from money_tracker.models import Transaction
from money_tracker.daos.base import AbsAccountsDAO, AbsTransactionsDAO, AbsTransactionCategoriesDAO

class TransactionsManager:

    accounts_dao: AbsAccountsDAO
    transactions_dao: AbsTransactionsDAO
    categories_dao: AbsTransactionCategoriesDAO

    def __init__(self, accounts_dao: AbsAccountsDAO, 
                 transactions_dao: AbsTransactionsDAO,
                 categories_dao: AbsTransactionCategoriesDAO) -> None:
        self.accounts_dao = accounts_dao
        self.transactions_dao = transactions_dao
        self.categories_dao = categories_dao

    def __add_transactions(transactions: List[Transaction]) -> List[Transaction]:
        pass

    def add_income(self, change: Decimal, execution_time: date,
                   account_id: str, category_id: str) -> Transaction:
        pass

    def add_expense(self, change: Decimal, account_id: str, category_id: str, 
                    execution_date: date)-> Transaction:
        pass

    def add_transfer(self, change: Decimal, from_account_id: str, 
                     to_account_id: str, execution_time: date) -> (Transaction, Transaction):
        pass
        
    def remove_transaction(transaction_id: str):
        pass

    def update_transaction(transaction_id: str, change: Decimal,
                           account_id: str, category_id: str,
                           execution_time: date):
        pass

    def get_transactions(account_id: str, start_date: date, end_date: str,
                         limit: int, offset: int) -> List[Transaction]:
        pass

    def move_transaction(transaction_id: str, account_id: str):
        pass

