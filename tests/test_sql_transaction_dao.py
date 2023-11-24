import unittest
from uuid import uuid4
from decimal import Decimal
from datetime import date, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from money_tracker.daos.sql_generic.dao import (
    GenericSQLCategoryDAO,
    GenericSQLAccountDAO,
    GenericSQLTransactionDAO,
)
from money_tracker.daos.sql_generic.models import Base, MappedTransaction
from money_tracker.models import Transaction
from tests.helpers import (
    load_initial_categories,
    load_initial_accounts,
    load_initial_transactions,
)


class TestSQLACategoryDAO(unittest.TestCase):
    initial_accounts = []

    def setUp(self) -> None:
        self.engine = create_engine("sqlite+pysqlite:///tests/test.db")
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

        self.dao = GenericSQLTransactionDAO(self.engine)

        # TODO load data without daos
        load_initial_categories(GenericSQLCategoryDAO(self.engine))
        load_initial_accounts(GenericSQLAccountDAO(self.engine))
        load_initial_transactions(self.dao)

    def test_create_single_transaction(self):
        attrs = {
            "change": Decimal("133.22"),
            "account_id": "123",
            "category_id": "234",
            "transaction_type": "inc",
            "description": "some description",
            "execution_date": date.today(),
            "group_id": None,
        }

        test_transaction = Transaction(**attrs)

        new_transaction = self.dao.save(test_transaction)

        self.assertIsNotNone(new_transaction.id)
        self.assertIsNotNone(new_transaction.creation_date)
        self.assertIsNone(new_transaction.group_id)
        self.assertEqual(Decimal("133.22"), new_transaction.change)

    def test_create_many_transactions(self):
        attr1 = {
            "change": Decimal("133.22"),
            "account_id": "123",
            "transaction_type": "tranin",
            "description": "some description",
            "execution_date": date.today(),
            "group_id": None,
        }
        attr2 = {
            "change": Decimal("-133.22"),
            "account_id": "234",
            "transaction_type": "tranout",
            "description": "some description",
            "execution_date": date.today(),
            "group_id": None,
        }

        transactions = [Transaction(**attr1), Transaction(**attr2)]

        new_transactions = self.dao.save_group(transactions)

        for new_transaction in new_transactions:
            self.assertIsNotNone(new_transaction.id)
            self.assertIsNotNone(new_transaction.group_id)

        self.assertEqual(new_transactions[0].group_id, new_transactions[1].group_id)

    def test_delete_transaction_in_group(self):
        attr1 = {
            "change": Decimal("133.22"),
            "account_id": "123",
            "transaction_type": "tranin",
            "description": "some description",
            "execution_date": date.today(),
            "group_id": None,
        }
        attr2 = {
            "change": Decimal("-133.22"),
            "account_id": "234",
            "transaction_type": "tranout",
            "description": "some description",
            "execution_date": date.today(),
            "group_id": None,
        }

        new_transactions = self.dao.save_group(
            [Transaction(**attr1), Transaction(**attr2)]
        )

        with Session(self.dao.engine) as session:
            self.assertIsNotNone(session.get(MappedTransaction, new_transactions[0].id))
            self.assertIsNotNone(session.get(MappedTransaction, new_transactions[1].id))

        self.dao.delete(new_transactions[0])

        with Session(self.dao.engine) as session:
            self.assertIsNone(session.get(MappedTransaction, new_transactions[0].id))
            self.assertIsNone(session.get(MappedTransaction, new_transactions[1].id))

    def test_delete_transaction(self):
        test_transaction = self.dao.get("123")

        self.dao.delete(test_transaction)

        with Session(self.engine) as session:
            self.assertIsNone(session.get(MappedTransaction, 123))

    def test_get_transactions_for_an_account(self):
        test_account_id = "123"
        transactions = self.dao.filter(account_id="123", limit=5)

        self.assertEqual(2, len(transactions))

        for t in transactions:
            self.assertEqual(test_account_id, t.account_id)

    def test_get_transactions_by_date(self):
        start_date = date(2023, 3, 3)
        end_date = date(2023, 12, 31)
        transactions = self.dao.filter(start_date=start_date, end_date=end_date)

        self.assertEqual(3, len(transactions))

        for t in transactions:
            self.assertGreaterEqual(t.execution_date, start_date)
            self.assertLessEqual(t.execution_date, end_date)

    def test_wrong_dates_in_filter_raises_exception(self):
        with self.assertRaises(Exception):
            self.dao.filter(start_date=date(2023, 12, 1), end_date=date(2023, 1, 1))

    def test_default_ordering_by_execution_date(self):
        transactions = self.dao.filter()

        for i, _ in enumerate(transactions):
            if len(transactions) != i + 1:
                self.assertGreater(
                    transactions[i].execution_date, transactions[i + 1].execution_date
                )

    def tearDown(self) -> None:
        Base.metadata.drop_all(self.engine)
