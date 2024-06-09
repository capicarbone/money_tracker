from ast import Dict
from decimal import Decimal
from typing import List
from datetime import date, datetime

from money_tracker.models import (
    ACCOUNT_TYPES_DICT,
    Account,
    HIGH_LIQUIDITY_TYPE,
    ACCOUNT_TYPES,
    CHECKING_ACCOUNT_TYPE,
    LIABILITY_ACCOUNT_TYPE,
)
from money_tracker.daos.base import AbsAccountsDAO


class AccountsManager:

    def __init__(self, accounts_dao: AbsAccountsDAO) -> None:
        self.accounts_dao = accounts_dao

    def get_all(self) -> List[Account]:
        return self.accounts_dao.get_all()

    def exists(self, id) -> bool:
        return self.accounts_dao.exists(id)

    def get_by_name(self, name) -> Account:
        """
        Get an account by name.
        """

        accounts = self.get_all()

        try:
            return next(filter(lambda x: x.name.lower() == name.lower(), accounts))
        except StopIteration:
            raise Exception(f"Account not found by name {name}")

    def get_types(self) -> Dict:
        return ACCOUNT_TYPES_DICT

    def create_account(
        self,
        name,
        account_type: str,
        liquidity_type=HIGH_LIQUIDITY_TYPE,
        initial_balance=Decimal("0.00"),
    ) -> Account:
        creation_date = datetime.now()

        if account_type not in ACCOUNT_TYPES:
            raise Exception("Invalid account type.")

        new_account = Account(
            name=name,
            account_type=account_type,
            creation_date=creation_date,
            liquidity_type=liquidity_type,
            balance=initial_balance,
        )

        return self.accounts_dao.save(new_account)

    def create_checking_account(self, name: str) -> Account:
        return self.create_account(name, CHECKING_ACCOUNT_TYPE)

    def create_liability_account(self, name: str) -> Account:
        return self.create_account(name, LIABILITY_ACCOUNT_TYPE)

    # TODO add investment account creation
    # add savings account creation
