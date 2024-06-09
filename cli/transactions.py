from datetime import datetime, date, timedelta
from decimal import Decimal
from typing_extensions import Annotated
from sqlalchemy import true
import typer
from cli.utils import as_json_list, format_amount, instance_dao_factory

from money_tracker import MoneyTracker
from money_tracker.daos.sql_generic.factory import SQLiteDAOFactory
from money_tracker.models import EXPENSE_CATEGORY, INCOME_CATEGORY, Account, Category

app = typer.Typer()


def get_category(tracker:MoneyTracker, category_id, category_name) -> Category:
    if not category_id:
        try:
            return tracker.categories.get_by_name(category_name)
        except Exception:
            pass
    else:
        if tracker.categories.exists(category_id):
            return tracker.categories.get(category_id)

    return None


def get_account(tracker: MoneyTracker, account_id, account_name) -> Account:
    if not account_id:
        try:
            return tracker.accounts.get_by_name(account_name)
        except Exception:
            pass
    else:
        if tracker.accounts.exists(account_id):
            return tracker.accounts.get_all()

    return None


def get_execution_date(execution_date: datetime, days_ago: int) -> date:

    if days_ago:
        return date.today() - timedelta(days=days_ago)

    elif execution_date:
        return date(
            year=(
                execution_date.year
                if execution_date.year != 1900
                else datetime.now().year
            ),
            month=execution_date.month,
            day=execution_date.day,
        )
    else:
        raise Exception("Invalid execution_date")


def add_income_or_expense(
    source: str,
    is_income: bool,
    amount: str,
    description: str,
    account_name: str,
    account_id: str,
    category_name: str,
    category_id: str,
    execution_date: datetime,
    days_ago: int,
):
    
    tracker = MoneyTracker(instance_dao_factory(source))

    d_amount = Decimal(amount) if is_income else -Decimal(amount)

    if not account_name and not account_id:
        raise Exception(
            "Account is missing, please specify account-name or account-id parameter."
        )

    if not category_name and not category_id:
        raise Exception(
            "Category is missing, please specify category-name or category-id parameter."
        )

    account = get_account(tracker, account_id, account_name)
    category = get_category(tracker, category_id, category_name)

    if not account:
        raise Exception("Account not found")

    if not category:
        raise Exception("Category not found")

    if is_income and category.category_type == EXPENSE_CATEGORY:
        raise Exception("Category must be for incomes.")

    if not is_income and category.category_type == INCOME_CATEGORY:
        raise Exception("Category must be for expenses.")

    try:
        d_execution_date = get_execution_date(execution_date, days_ago)
    except Exception:
        raise Exception("Invalid date.")

    transaction_parameters = {
        "change": d_amount,
        "execution_date": d_execution_date,
        "account_id": account.id,
        "category_id": category.id,
        "description": description,
    }

    new_transaction = (
        tracker.transactions.add_income(**transaction_parameters)
        if is_income
        else tracker.transactions.add_expense(**transaction_parameters)
    )

    print(new_transaction.model_dump_json())


# ------ Comands ------


@app.command("receive")
def add_income(
    source: Annotated[str, typer.Option()],
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
    try:
        add_income_or_expense(
            source=source,
            is_income=True,
            amount=amount,
            description=description,
            account_name=account_name,
            account_id=account_id,
            category_id=category_id,
            category_name=category_name,
            execution_date=execution_date,
            days_ago=days_ago,
        )
    except Exception as ex:
        print(ex)


@app.command("spend")
def add_expense(
    source: Annotated[str, typer.Option()],
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
    
    try:
        add_income_or_expense(
            source=source,
            is_income=False,
            amount=amount,
            description=description,
            account_name=account_name,
            account_id=account_id,
            category_id=category_id,
            category_name=category_name,
            execution_date=execution_date,
            days_ago=days_ago,
        )

    except Exception as ex:
        print(ex)


@app.command("transfer")
def add_transfer(
    source: Annotated[str, typer.Option()],
    amount: Annotated[str, typer.Argument()],
    description: Annotated[str, typer.Argument()] = "",
    from_account_name: Annotated[str, typer.Option()] = None,
    from_account_id: Annotated[str, typer.Option()] = None,
    to_account_name: Annotated[str, typer.Option()] = None,
    to_account_id: Annotated[str, typer.Option()] = None,
    execution_date: Annotated[
        datetime, typer.Option(metavar="date", formats=["%Y-%m-%d", "%m-%d"])
    ] = datetime.now(),
    days_ago: Annotated[int, typer.Option()] = None,
):
    tracker = MoneyTracker(instance_dao_factory(source))
    d_amount = Decimal(amount)

    from_account = get_account(tracker, from_account_id, from_account_name)
    to_account = get_account(tracker, to_account_id, to_account_name)

    if not from_account or not to_account:
        print("Account not found.")
    try:

        d_execution_date = get_execution_date(execution_date, days_ago)

        transfer_in, transfer_out = tracker.transactions.add_transfer(
            change=d_amount,
            description=description,
            execution_date=d_execution_date,
            from_account_id=from_account.id,
            to_account_id=to_account.id,
        )

        print(as_json_list([transfer_in, transfer_out]))

    except Exception as ex:
        print(ex)


@app.command()
def list(
    source: Annotated[str, typer.Option()],
    limit: Annotated[int, typer.Option()] = 20, 
         offset: Annotated[int, typer.Option()] = 0):
    
    tracker = MoneyTracker(instance_dao_factory(source))
    transactions = tracker.transactions.get_transactions(limit=limit, offset=offset)

    print(as_json_list(transactions))
