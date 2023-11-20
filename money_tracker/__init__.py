from money_tracker.daos.base import AbsDAOFactory
from money_tracker.managers.accounts import AccountsManager
from money_tracker.managers.categories import TransactionCategoriesManager
from money_tracker.managers.transactions import TransactionsManager


class MoneyTracker:
    transactions: TransactionsManager = None
    accounts: AccountsManager = None
    categories: TransactionCategoriesManager = None

    def __init__(self, daos_factory: AbsDAOFactory) -> None:
        self.transactions = TransactionsManager(
            accounts_dao=daos_factory.get_account_dao(),
            transactions_dao=daos_factory.get_transaction_dao(),
            categories_dao=daos_factory.get_category_dao(),
        )

        self.accounts = AccountsManager(
            accounts_dao=daos_factory.get_account_dao()
        )

        self.categories = TransactionCategoriesManager(
            categories_dao=daos_factory.get_category_dao()
        )
