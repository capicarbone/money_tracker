from curses import reset_shell_mode
import unittest

from sqlalchemy import create_engine

from money_tracker.daos.sql_generic.dao import GenericSQLCategoryDAO
from money_tracker.daos.sql_generic.models import Base, MappedCategory
from money_tracker.models import Category
from sqlalchemy.orm import Session
from tests.helpers import load_initial_categories


class TestSQLACategoryDAO(unittest.TestCase):
    initial_accounts = []

    def setUp(self) -> None:
        self.engine = create_engine("sqlite+pysqlite:///tests/test.db")
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

        self.dao = GenericSQLCategoryDAO(self.engine)

        load_initial_categories(self.dao)

    def test_create_valid_category(self):
        attrs = {"name": "Travel", "parent_category_id": None, "category_type": "exp"}

        test_category = Category(**attrs)
        saved_category = self.dao.save(test_category)

        self.assertIsNotNone(saved_category.id)

        with Session(self.engine) as session:
            db_entity = session.get(MappedCategory, saved_category.id)
            for attr, value in attrs.items():
                self.assertEqual(getattr(db_entity, attr), value)

    def test_create_valid_category_with_parent(self):
        attrs = {"name": "Travel", "parent_category_id": "345", "category_type": "exp"}

        test_category = Category(**attrs)
        saved_category = self.dao.save(test_category)

        self.assertIsNotNone(saved_category.id)

        with Session(self.engine) as session:
            db_entity = session.get(MappedCategory, saved_category.id)
            for attr, value in attrs.items():
                if attr == "parent_category_id":
                    self.assertEqual(str(getattr(db_entity, attr)), value)
                else:
                    self.assertEqual(getattr(db_entity, attr), value)

    def test_exists(self):
        result = self.dao.exists("123")
        self.assertTrue(result)

        result = self.dao.exists("777")
        self.assertFalse(result)

    def test_get_all(self):
        categories = self.dao.get_all()
        self.assertEqual(4, len(categories))

    def tearDown(self) -> None:
        Base.metadata.drop_all(self.engine)
