
import unittest

from .helpers import load_initial_categories

from money_tracker.models import EXPENSE_CATEGORY, INCOME_CATEGORY, Category
from money_tracker.daos.inmemory import InMemoryTransactionCategoriesDAO
from money_tracker.managers import TransactionCategoriesManager

class TestCategoryManager(unittest.TestCase):

    manager: TransactionCategoriesManager = None

    def setUp(self) -> None:
        dao = InMemoryTransactionCategoriesDAO()
        self.manager = TransactionCategoriesManager(dao)

        load_initial_categories(dao)


    def test_get_all(self):
        categories = self.manager.get_all()        

        self.assertEqual(4, len(categories))

    def test_create_valid_expense_category(self):
        
        expense = self.manager.create_expense_category("Coffe")

        self.assertIsNotNone(expense.id)
        self.assertEqual(expense.category_type, EXPENSE_CATEGORY)

    def test_create_valid_income_category(self):
      
        income = self.manager.create_income_category("Service", None)

        self.assertIsNotNone(income.id)
        self.assertEqual(income.category_type, INCOME_CATEGORY)


    def test_create_valid_category_with_parent(self):
        
        parent = self.manager.create_income_category("Parent")
        child = self.manager.create_income_category("child", parent.id)

        self.assertIsNotNone(child.parent_category_id)

    def tearDown(self) -> None:
        InMemoryTransactionCategoriesDAO().clear()

    
    # TODO tests to add
    # parent with different type
    # many levels of hirarchy
    # change name
    # remove category
    

if __name__ == '__main__':
    unittest.main()