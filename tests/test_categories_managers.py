
import unittest
from money_tracker.models import EXPENSE_CATEGORY, INCOME_CATEGORY
from money_tracker.daos.inmemory import InMemoryTransactionsDAO
from money_tracker.managers.categories import TransactionCategoriesManager

class TestCategoryManager(unittest.TestCase):

    @property
    def manager(self) -> TransactionCategoriesManager:
        dao = InMemoryTransactionsDAO()
        return TransactionCategoriesManager(dao)

    def test_create_expense_category(self):
        
        expense = self.manager.create_expense_category("Coffe")

        self.assertIsNotNone(expense.id)
        self.assertEqual(expense.category_type, EXPENSE_CATEGORY)

    def test_create_income_category(self):
      
        income = self.manager.create_income_category("Service")

        self.assertIsNotNone(income.id)
        self.assertEqual(income.category_type, INCOME_CATEGORY)


    def test_create_category_with_parent(self):
        
        parent = self.manager.create_income_category("Parent")
        child = self.manager.create_income_category("child", parent.id)

        self.assertIsNotNone(child.parent_category_id)

    # TODO tests to add
    # parent with different type
    # change name
    # remove category
    



if __name__ == '__main__':
    unittest.main()