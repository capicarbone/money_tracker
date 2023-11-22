from typing import List
from datetime import date, datetime

from money_tracker.models import (
    Account,
    HIGH_LIQUIDITY_TYPE,
    ACCOUNT_TYPES,
    CHECKING_ACCOUNT_TYPE,
    LIABILITY_ACCOUNT_TYPE,
)
from money_tracker.daos.base import AbsAccountsDAO


class AccountsManager:
    accounts_dao: AbsAccountsDAO = None

    def __init__(self, accounts_dao: AbsAccountsDAO) -> None:
        self.accounts_dao = accounts_dao

    def get_all(self) -> List[Account]:
        return self.accounts_dao.get_all()

    def create_account(
        self, name, account_type: str, liquidity_type=HIGH_LIQUIDITY_TYPE
    ) -> Account:
        creation_date = datetime.now()

        if account_type not in ACCOUNT_TYPES:
            raise Exception("Invalid account type.")

        new_account = Account(
            name=name,
            account_type=account_type,
            creation_date=creation_date,
            liquidity_type=liquidity_type,
        )

        return self.accounts_dao.save(new_account)

    def create_checking_account(self, name: str) -> Account:
        return self.create_account(name, CHECKING_ACCOUNT_TYPE)

    def create_liability_account(self, name: str) -> Account:
        return self.create_account(name, LIABILITY_ACCOUNT_TYPE)

    # TODO add investment account creation
    # add savings account creation
