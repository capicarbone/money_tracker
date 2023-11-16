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

    def tearDown(self) -> None:
        Base.metadata.drop_all(self.engine)
