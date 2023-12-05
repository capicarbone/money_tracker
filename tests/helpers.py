from datetime import datetime, date

from money_tracker.models import (
    Transaction,
    EXPENSE_CATEGORY,
    INCOME_CATEGORY,
    Category,
    Account,
    CHECKING_ACCOUNT_TYPE,
    LIABILITY_ACCOUNT_TYPE,
    INCOME_TRANSACTION_TYPE,
    EXPENSE_TRANSACTION_TYPE,
    TRANSFER_IN_TRANSACTION_TYPE,
    TRANSFER_OUT_TRANSACTION_TYPE,
)
from money_tracker.daos import (
    AbsTransactionCategoryDAO,
    AbsAccountsDAO,
    AbsTransactionsDAO,
)


def load_initial_categories(dao: AbsTransactionCategoryDAO):
    test_data = [
        Category(id="123", name="Services", category_type=INCOME_CATEGORY),
        Category(
            id="234",
            name="My work",
            category_type=INCOME_CATEGORY,
            parent_category_id="123",
        ),
        Category(id="345", name="Home", category_type=EXPENSE_CATEGORY),
        Category(
            id="456",
            name="Groceries",
            category_type=EXPENSE_CATEGORY,
            parent_category_id="345",
        ),
    ]

    for e in test_data:
        dao.save(e)


def load_initial_accounts(dao: AbsAccountsDAO):
    test_data = [
        Account(
            id="123",
            name="Blue Bank",
            creation_date=datetime.now(),
            account_type=CHECKING_ACCOUNT_TYPE,
        ),
        Account(
            id="234",
            name="Green Bank",
            creation_date=datetime.now(),
            account_type=LIABILITY_ACCOUNT_TYPE,
        ),
    ]

    for e in test_data:
        dao.save(e)


def load_initial_transactions(dao: AbsTransactionsDAO):
    test_data = [
        [
            Transaction(
                id="123",
                change=200,
                account_id="123",
                category_id="234",
                transaction_type=INCOME_TRANSACTION_TYPE,
                description="test transaction",
                execution_date=date(2023, 2, 2),
            )
        ],
        [
            Transaction(
                id="234",
                change=-100,
                account_id="123",
                category_id="456",
                transaction_type=EXPENSE_TRANSACTION_TYPE,
                description="test transaction",
                execution_date=date(2023, 1, 1),
            )
        ],[
        Transaction(
            id="345",
            change=700,
            account_id="234",
            category_id="234",
            transaction_type=INCOME_TRANSACTION_TYPE,
            description="test transaction",
            execution_date=date(2023, 5, 5),
        )],
        [
            Transaction(
                id="456",
                change=-444.20,
                account_id="234",
                category_id="234",
                transaction_type=EXPENSE_TRANSACTION_TYPE,
                description="test transaction",
                execution_date=date(2023, 4, 4),
            )
        ],
        [
            Transaction(
                id="567",
                change=-222.20,
                account_id="234",
                category_id="234",
                transaction_type=EXPENSE_TRANSACTION_TYPE,
                description="test transaction",
                execution_date=date(2023, 3, 3),
            )
        ],
    ]

    for e in test_data:
        dao.save_group(e)
