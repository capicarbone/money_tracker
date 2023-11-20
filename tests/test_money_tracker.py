import unittest

from money_tracker import MoneyTracker
from money_tracker.daos.sql_generic.factory import SQLiteDAOFactory
from money_tracker.managers.accounts import AccountsManager
from money_tracker.managers.categories import TransactionCategoriesManager
from money_tracker.managers.transactions import TransactionsManager

class MoneyTrackerTest(unittest.TestCase):

    def test_init(self):
        factory = SQLiteDAOFactory("test.db")
        tracker = MoneyTracker(factory)

        self.assertIsInstance(tracker.accounts, AccountsManager)
        self.assertIsInstance(tracker.categories, TransactionCategoriesManager)
        self.assertIsInstance(tracker.transactions, TransactionsManager)