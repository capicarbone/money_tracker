
import unittest
from money_tracker.models import EXPENSE_CATEGORY, INCOME_CATEGORY, Category
from money_tracker.daos.inmemory import InMemoryTransactionCategoriesDAO, global_simple_storage
from money_tracker.managers.categories import TransactionCategoriesManager

class TestCategoryManager(unittest.TestCase):

    manager: TransactionCategoriesManager = None

    def setUp(self) -> None:
        self.dao = InMemoryTransactionCategoriesDAO()
        self.manager = TransactionCategoriesManager(self.dao)

        test_data = [
            Category(
                id="123",
                name="Services",
                category_type=INCOME_CATEGORY
            ),
            Category(
                id='234',
                name='My work',
                category_type=INCOME_CATEGORY,
                parent_category_id='123'
            ),
            Category(
                id='345',
                name='Home',
                category_type=EXPENSE_CATEGORY
            ),
            Category(
                id='456',
                name='Groceries',
                category_type=EXPENSE_CATEGORY,
                parent_category_id='345'
            )
        ]

        for e in test_data:
            self.dao.save(e)


    def test_get_all(self):
        categories = self.manager.get_all()
        print(categories)

        self.assertEqual(4, len(categories))

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

    def tearDown(self) -> None:
        self.dao.clear()

    
    # TODO tests to add
    # parent with different type
    # many levels of hirarchy
    # change name
    # remove category
    

if __name__ == '__main__':
    unittest.main()