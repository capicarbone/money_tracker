import unittest
from money_tracker.daos.sql_generic.dao import GenericSQLAccountDAO, GenericSQLCategoryDAO, GenericSQLTransactionDAO
from money_tracker.daos.sql_generic import SQLiteDAOFactory


class SqliteDAOFactoryTest(unittest.TestCase):
    def test_get_account_dao(self):
        factory = SQLiteDAOFactory("test.db")

        dao = factory.get_account_dao()

        self.assertIsInstance(dao, GenericSQLAccountDAO)

    
    def test_get_category_dao(self):
        factory = SQLiteDAOFactory("test.db")

        dao = factory.get_category_dao()

        self.assertIsInstance(dao, GenericSQLCategoryDAO)


    def test_get_category_dao(self):
        factory = SQLiteDAOFactory("test.db")

        dao = factory.get_transaction_dao()

        self.assertIsInstance(dao, GenericSQLTransactionDAO)