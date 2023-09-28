from typing import List
from money_tracker.daos.base import AbsTransactionCategoriesDAO
from money_tracker.models import Category, EXPENSE_CATEGORY, INCOME_CATEGORY

class TransactionCategoriesManager:
    categories_dao : AbsTransactionCategoriesDAO

    def __init__(self, categories_dao: AbsTransactionCategoriesDAO) -> None:
        self.categories_dao = categories_dao

    def get_all(self) -> List[Category]:
        # TODO get in hierarchy.
        return self.categories_dao.get_all()
    
    def create_category(self, name: str, category_type: str, parent_category_id=None) -> Category:
        if self.categories_dao.exists(parent_category_id):
            parent_category : Category = self.categories_dao.get(parent_category_id)
            if parent_category.category_type != category_type:
                raise Exception("Parent category must belong to the same type.")

        new_category = Category(name=name, category_type=category_type, parent_category_id=parent_category_id)
        return self.categories_dao.save(new_category)

    def create_expense_category(self, name: str, parent_category_id: str = None) -> Category:
        return self.create_category(name=name, category_type=EXPENSE_CATEGORY, parent_category_id=parent_category_id)
    
    def create_income_category(self, name: str, parent_category_id: str = None) -> Category:
        return self.create_category(name=name, category_type=INCOME_CATEGORY, parent_category_id=parent_category_id)
    

        
