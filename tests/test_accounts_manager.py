import unittest
from datetime import datetime

from .helpers import load_initial_accounts
from money_tracker.models import Account, LIABILITY_ACCOUNT_TYPE, CHECKING_ACCOUNT_TYPE, ACCOUNT_TYPES_DICT
from money_tracker.daos.inmemory import InMemoryAccountsDAO
from money_tracker.managers import AccountsManager

class TestAccountssManager(unittest.TestCase):
    
    def setUp(self) -> None:
        dao = InMemoryAccountsDAO()
        self.manager = AccountsManager(dao)
            
        load_initial_accounts(dao)

    def test_get_all(self):
        accounts = self.manager.get_all()        

        self.assertEqual(2, len(accounts))

    def test_get_types_dict(self):
        types = self.manager.get_types()

        self.assertEqual(types, ACCOUNT_TYPES_DICT)

    def test_create_checking_account(self):
        account = self.manager.create_checking_account("Red Bank")

        self.assertIsNotNone(account.id)
        self.assertEqual(account.account_type, CHECKING_ACCOUNT_TYPE)


    def test_create_checking_account(self):
        account = self.manager.create_liability_account("Red Bank")

        self.assertIsNotNone(account.id)
        self.assertEqual(account.account_type, LIABILITY_ACCOUNT_TYPE)



    def tearDown(self) -> None:
        InMemoryAccountsDAO().clear()

if __name__ == '__main__':
    unittest.main()