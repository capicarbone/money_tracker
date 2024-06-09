import json
import typer
from typing_extensions import Annotated
from cli.utils import as_json_list, instance_dao_factory
from money_tracker import MoneyTracker


app = typer.Typer()


@app.command("add-income-type")
def add_income_category(
    source: Annotated[str, typer.Option()],
    name: Annotated[str, typer.Argument()],
    parent_category_id: Annotated[str, typer.Argument()] = None,
):

    tracker = MoneyTracker(instance_dao_factory(source))

    new_category = tracker.categories.create_income_category(
        name, parent_category_id=parent_category_id
    )

    print(new_category.model_dump_json())


@app.command("add-expense-type")
def add_expense_category(
    source: Annotated[str, typer.Option()],
    name: Annotated[str, typer.Argument()],
    parent_category_id: Annotated[str, typer.Argument()] = None,
):
    tracker = MoneyTracker(instance_dao_factory(source))
    new_category = tracker.categories.create_expense_category(
        name, parent_category_id=parent_category_id
    )

    print(new_category.model_dump_json())


@app.command("list")
def list_all(
    source: Annotated[str, typer.Option()],
):
    tracker = MoneyTracker(instance_dao_factory(source))
    categories = tracker.categories.get_all()

    print(as_json_list(categories))


@app.command("types")
def list_types(
    source: Annotated[str, typer.Option()],
):
    """
    List category types.
    """
    tracker = MoneyTracker(instance_dao_factory(source))
    types = tracker.categories.get_types()

    print(json.dumps(types))
