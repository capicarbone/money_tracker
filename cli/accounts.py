from decimal import Decimal
import typer
from typing_extensions import Annotated
from money_tracker import MoneyTracker
from money_tracker.daos.sql_generic.factory import SQLiteDAOFactory

from money_tracker.models import CHECKING_ACCOUNT, HIGH_LIQUIDITY_TYPE

app = typer.Typer()


@app.command("add")
def add_account(
    name: Annotated[str, typer.Argument()],
    account_type: Annotated[str, typer.Argument()] = CHECKING_ACCOUNT,
    liquidity_type: Annotated[str, typer.Argument()] = HIGH_LIQUIDITY_TYPE
):
    """
    Create a new account.
    """
    factory = SQLiteDAOFactory("test.db")
    tracker = MoneyTracker(factory)

    new_account = tracker.accounts.create_account(name, account_type, liquidity_type)

    account_type_name = tracker.accounts.get_types()[account_type]
    print(f"{new_account.name}({account_type_name}) created with initial balance of {new_account.balance}")


@app.command("list")
def list_all():
    """
    It lists all accounts.
    """
    factory = SQLiteDAOFactory("test.db")
    tracker = MoneyTracker(factory)

    accounts = tracker.accounts.get_all()

    for account in accounts:
        # TODO print as table with rich
        print(f"{account.id}: {account.name}")


@app.command("balances")
def balances():
    """
    List all account with balances.
    """
    factory = SQLiteDAOFactory("test.db")
    tracker = MoneyTracker(factory)

    accounts = tracker.accounts.get_all()

    for account in accounts:
        print(f"{account.name}: {account.balance}")

@app.command("types")
def list_types():
    """
    It lists all account types.
    """
    factory = SQLiteDAOFactory("test.db")
    tracker = MoneyTracker(factory)

    print("Available account types:")
    for value, name in tracker.accounts.get_types().items():
        print(f"{value}: {name}")
