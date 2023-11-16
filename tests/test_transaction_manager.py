import unittest
from decimal import *
from datetime import date
from .helpers import (
    load_initial_accounts,
    load_initial_categories,
    load_initial_transactions,
)

from money_tracker.models import Transaction
from money_tracker.managers import TransactionsManager
from money_tracker.daos.inmemory import (
    InMemoryTransactionsDAO,
    InMemoryTransactionCategoriesDAO,
    InMemoryAccountsDAO,
)

getcontext().traps[FloatOperation] = True


class TestTransactionsManager(unittest.TestCase):
    manager: TransactionsManager = None

    def setUp(self) -> None:
        load_initial_accounts(InMemoryAccountsDAO())
        load_initial_categories(InMemoryTransactionCategoriesDAO())
        load_initial_transactions(InMemoryTransactionsDAO())

        self.manager = TransactionsManager(
            transactions_dao=InMemoryTransactionsDAO(),
            accounts_dao=InMemoryAccountsDAO(),
            categories_dao=InMemoryTransactionCategoriesDAO(),
        )

    def tearDown(self) -> None:
        InMemoryAccountsDAO().clear()
        InMemoryTransactionCategoriesDAO().clear()
        InMemoryTransactionsDAO().clear()

    def test_add_valid_income(self):
        income = self.manager.add_income(
            change=Decimal("223.12"),
            execution_date=date(2023, 10, 1),
            account_id="123",
            category_id="123",
            description="Some description",
        )

        self.assertIsNotNone(income.id)

    def test_add_valid_expense(self):
        expense = self.manager.add_expense(
            change=Decimal("122.23"),
            execution_date=date(2023, 10, 1),
            account_id="123",
            category_id="456",
            description="Some description",
        )

        self.assertIsNotNone(expense.id)

    def test_add_valid_transfer(self):
        transfer_in, transfer_out = self.manager.add_transfer(
            change=Decimal("222.23"),
            from_account_id="123",
            to_account_id="234",
            execution_date=date(2023, 10, 1),
        )

        self.assertIsNotNone(transfer_in)
        self.assertIsNotNone(transfer_in.id)
        self.assertIsNotNone(transfer_out)
        self.assertIsNotNone(transfer_out.id)
        self.assertEqual(transfer_in.account_id, "234")
        self.assertEqual(transfer_out.account_id, "123")

    def test_get_transactions_by_account(self):
        test_account_id = "123"

        transactions = self.manager.get_transactions(account_id=test_account_id)

        self.assertEqual(2, len(transactions))

        for t in transactions:
            self.assertEqual(test_account_id, t.account_id)

    def test_remove_existing_transaction(self):
        test_transaction_id = "123"

        self.manager.remove_transaction(test_transaction_id)

        total_transactions = len(self.manager.get_transactions())

        self.assertEqual(4, total_transactions)

    def test_change_amount(self):
        test_transaction_id = "123"

        dao = InMemoryTransactionsDAO()
        original_change = dao.get(test_transaction_id).change

        new_change = Decimal("777.12")

        self.manager.update_transaction(
            transaction_id=test_transaction_id, change=new_change
        )

        changed_transaction = dao.get(test_transaction_id)

        self.assertEqual(new_change, changed_transaction.change)
        self.assertNotEqual(original_change, changed_transaction.change)

    def test_move_transaction(self):
        test_transaction_id = "123"
        new_account_id = "234"

        self.manager.move_transaction(test_transaction_id, new_account_id)

        moved_transaction: Transaction = InMemoryTransactionsDAO().get(
            test_transaction_id
        )

        self.assertEqual(moved_transaction.account_id, new_account_id)

    # TODO transactions with differente limit and offset
