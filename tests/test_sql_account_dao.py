import unittest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from tests.helpers import load_initial_accounts
from money_tracker.daos.sql_generic.dao import GenericSQLAccountDAO
import money_tracker.daos.sql_generic.models as db

from money_tracker.models import Account


class TestSQLAccountDAO(unittest.TestCase):    

    def setUp(self) -> None:
        self.engine = create_engine("sqlite+pysqlite:///tests/test.db")
        db.Base.metadata.drop_all(self.engine)
        db.Base.metadata.create_all(self.engine)

        self.dao = GenericSQLAccountDAO(self.engine)

        load_initial_accounts(self.dao)

    def test_create_valid_account(self):
        attrs = {
            "name": "Blue Bank",
            "creation_date": date.today(),
            "account_type": "CH",
            "liquidity_type": "high",
        }

        test_account = Account(**attrs)
        saved_account = self.dao.save(test_account)

        self.assertIsNotNone(saved_account.id)

        with Session(self.engine) as session:
            db_entity = session.get(db.MappedAccount, saved_account.id)
            for attr, value in attrs.items():
                self.assertEqual(getattr(db_entity, attr), value)

    def test_get_all(self):
        accounts = self.dao.get_all()

        self.assertEqual(2, len(accounts), "Wrong account count.")

    def test_exists(self):
        result = self.dao.exists("234")

        self.assertTrue(result)

        result = self.dao.exists("777")

        self.assertFalse(result)

    def tearDown(self) -> None:
        db.Base.metadata.drop_all(self.engine)


