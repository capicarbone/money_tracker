import json
import typer
from typing_extensions import Annotated
from cli.utils import as_json_list
from money_tracker import MoneyTracker
from money_tracker.daos.sql_generic.factory import SQLiteDAOFactory

from money_tracker.models import CHECKING_ACCOUNT, HIGH_LIQUIDITY_TYPE

app = typer.Typer()
tracker = MoneyTracker(SQLiteDAOFactory("test.db"))


@app.command("add")
def add_account(
    name: Annotated[str, typer.Argument()],
    account_type: Annotated[str, typer.Argument()] = CHECKING_ACCOUNT,
    liquidity_type: Annotated[str, typer.Argument()] = HIGH_LIQUIDITY_TYPE
):
    """
    Create a new account.
    """

    new_account = tracker.accounts.create_account(name, account_type.upper(), liquidity_type)

    print(new_account.model_dump_json())

@app.command("list")
def list_all():
    """
    List all accounts.
    """

    accounts = tracker.accounts.get_all()
    print(as_json_list(accounts))


@app.command("types")
def list_types():
    """
    List all account types.
    """
    
    print(json.dumps(tracker.accounts.get_types()))
