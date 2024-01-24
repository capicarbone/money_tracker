
import typer
from typing_extensions import Annotated
from money_tracker import MoneyTracker
from money_tracker.daos.sql_generic.factory import SQLiteDAOFactory

app = typer.Typer()
tracker = MoneyTracker(SQLiteDAOFactory("test.db"))

@app.command("add")
def add_category(
    name: Annotated[str, typer.Argument()],
    category_type: Annotated[str, typer.Argument()],
    parent_category: Annotated[str, typer.Argument()] = None
):
    pass

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
    