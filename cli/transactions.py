from datetime import datetime, date, timedelta
from decimal import Decimal
from typing_extensions import Annotated
import typer

from money_tracker import MoneyTracker
from money_tracker.daos.sql_generic.factory import SQLiteDAOFactory
from money_tracker.models import Account, Category

app = typer.Typer()
tracker = MoneyTracker(SQLiteDAOFactory("test.db"))


def get_category_id(category_id, category_name) -> Category:
    if not category_id:
        try:
            return tracker.categories.get_by_name(category_name).id
        except Exception:
            pass
    else:
        if tracker.categories.exists(category_id):
            return category_id

    return None


def get_account_id(account_id, account_name) -> Account:
    if not account_id:
        try:
            return tracker.accounts.get_by_name(account_name).id
        except Exception:
            pass
    else:
        if tracker.accounts.exists(account_id):
            return account_id

    return None


def get_execution_date(execution_date: datetime, days_ago: int) -> date:

    if days_ago:
        return date.today() - timedelta(days=days_ago)

    elif execution_date:
        return date(
            year=execution_date.year
            if execution_date.year != 1900
            else datetime.now().year,
            month=execution_date.month,
            day=execution_date.day,
        )
    else:
        raise Exception("Invalid execution_date")

 
# ------ Comands ------
    
@app.command("receive")
def add_income(
    amount: Annotated[str, typer.Argument()],
    description: Annotated[str, typer.Argument()] = "",
    account_name: Annotated[str, typer.Option()] = None,
    account_id: Annotated[str, typer.Option()] = None,
    category_id: Annotated[str, typer.Option()] = None,
    category_name: Annotated[str, typer.Option()] = None,
    execution_date: Annotated[
        datetime, typer.Option(metavar="date", formats=["%Y-%m-%d", "%m-%d"])
    ] = datetime.now(),
    days_ago: Annotated[int, typer.Option()] = None,
):
    d_amount = Decimal(amount)

    if not account_name and not account_id:
        print(
            "Account is missing, please specify account_name or account_id parameter."
        )
        return

    if not category_name and not category_id:
        print(
            "Category is missing, please specify category_name or category_id parameter."
        )
        return

    account_id = get_account_id(account_id, account_name)
    category_id = get_category_id(category_id, category_name)

    if not account_id:
        print("Account not found")
        return

    if not category_id:
        print("Category not found")
        return
    
    try:
        d_execution_date = get_execution_date(execution_date, days_ago)
    except Exception:
        print("Invalid date.")
        return

    tracker.transactions.add_income(
        change=d_amount,
        execution_date=d_execution_date,
        account_id=account_id,
        category_id=category_id,
        dsecription=description,
    )

    print("Added transaction")


@app.command("spend")
def add_expense(
    amount: Annotated[str, typer.Argument()],
    description: Annotated[str, typer.Argument()] = "",
    account_name: Annotated[str, typer.Option()] = None,
    account_id: Annotated[str, typer.Option()] = None,
    category_id: Annotated[str, typer.Option()] = None,
):
    pass
