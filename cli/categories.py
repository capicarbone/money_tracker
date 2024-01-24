import typer
from typing_extensions import Annotated
from money_tracker import MoneyTracker
from money_tracker.daos.sql_generic.factory import SQLiteDAOFactory

app = typer.Typer()
tracker = MoneyTracker(SQLiteDAOFactory("test.db"))


@app.command("add-income-type")
def add_income_category(
    name: Annotated[str, typer.Argument()],
    parent_category_id: Annotated[str, typer.Argument()] = None,
):
    new_category = tracker.categories.create_income_category(
        name, parent_category_id=parent_category_id
    )

    print(f"Income category {new_category.name} created.")


@app.command("add-expense-type")
def add_expense_category(
    name: Annotated[str, typer.Argument()],
    parent_category_id: Annotated[str, typer.Argument()] = None,
):
    new_category = tracker.categories.create_expense_category(
        name, parent_category_id=parent_category_id
    )

    print(f"Expense category {new_category.name} created.")


@app.command("list")
def list_all():
    categories = tracker.categories.get_all()

    for category in categories:
        print(f"{category.id}: {category.name}")


@app.command("types")
def list_types():
    """
    List category types.
    """
    types = tracker.categories.get_types()

    for value, name in types.items():
        print(f"{value}: {name}")
