import unittest
from datetime import datetime

from money_tracker.models import Account, LIABILITY_ACCOUNT_TYPE, CHECKING_ACCOUNT_TYPE
from money_tracker.daos.inmemory import InMemoryAccountsDAO
from money_tracker.managers import AccountsManager

class TestAccountssManager(unittest.TestCase):
    
    def setUp(self) -> None:
        self.dao = InMemoryAccountsDAO()
        self.manager = AccountsManager(self.dao)

        test_data = [
            Account(
                id="123",
                name="Blue Bank",
                creation_date=datetime.now(),
                account_type=CHECKING_ACCOUNT_TYPE
            ),
            Account(
                id="234",
                name="Green Bank",
                creation_date=datetime.now(),
                account_type=LIABILITY_ACCOUNT_TYPE
            ),
        ]

        for e in test_data:
            self.dao.save(e)

    def test_get_all(self):
        accounts = self.manager.get_all()        

        self.assertEqual(2, len(accounts))

    def test_create_checking_account(self):
        account = self.manager.create_checking_account("Red Bank")

        self.assertIsNotNone(account.id)
        self.assertEqual(account.account_type, CHECKING_ACCOUNT_TYPE)


    def test_create_checking_account(self):
        account = self.manager.create_liability_account("Red Bank")

        self.assertIsNotNone(account.id)
        self.assertEqual(account.account_type, LIABILITY_ACCOUNT_TYPE)



    def tearDown(self) -> None:
        self.dao.clear()

if __name__ == '__main__':
    unittest.main()