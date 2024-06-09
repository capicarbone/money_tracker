from typing import List
from money_tracker.daos.base import AbsTransactionCategoryDAO
from money_tracker.models import (
    Category,
    EXPENSE_CATEGORY,
    INCOME_CATEGORY,
    CATEGORY_TYPES_DICT,
)


class TransactionCategoriesManager:

    def __init__(self, categories_dao: AbsTransactionCategoryDAO) -> None:
        self.categories_dao = categories_dao

    def get_all(self) -> List[Category]:
        return self.categories_dao.get_all()

    def exists(self, category_id) -> bool:
        return self.categories_dao.exists(category_id)

    def get(self, category_id) -> Category:
        return next(iter([x for x in self.get_all() if x.id == category_id]))

    def get_by_name(self, name) -> Category:

        categories = self.get_all()

        try:
            return next(filter(lambda x: x.name.lower() == name.lower(), categories))
        except StopIteration:
            raise Exception(f"Category not found by name {name}")

    def create_category(
        self, name: str, category_type: str, parent_category_id=None
    ) -> Category:
        if self.categories_dao.exists(parent_category_id):
            parent_category: Category = self.categories_dao.get(parent_category_id)
            if parent_category.category_type != category_type:
                raise Exception("Parent category must belong to the same type.")

            if parent_category.parent_category_id is not None:
                raise Exception("More than one level of hierarchy not allowed.")

        new_category = Category(
            name=name,
            category_type=category_type,
            parent_category_id=parent_category_id,
        )
        return self.categories_dao.save(new_category)

    def create_expense_category(
        self, name: str, parent_category_id: str = None
    ) -> Category:
        return self.create_category(
            name=name,
            category_type=EXPENSE_CATEGORY,
            parent_category_id=parent_category_id,
        )

    def create_income_category(
        self, name: str, parent_category_id: str = None
    ) -> Category:
        return self.create_category(
            name=name,
            category_type=INCOME_CATEGORY,
            parent_category_id=parent_category_id,
        )

    def get_types(self):
        return CATEGORY_TYPES_DICT
