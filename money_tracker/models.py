from uuid import UUID
from typing import Literal, Optional
from decimal import Decimal

from datetime import datetime, date
from pydantic import BaseModel

CHECKING_ACCOUNT = "CH"
SAVING_ACCOUNT = "SV"
LIABILITIES_ACCOUNT = "LB"
INVESTMENT_ACCOUNT = "IV"

HIGH_LIQUIDITY_TYPE = "high"

CHECKING_ACCOUNT_TYPE = "CH"
SAVINGS_ACCOUNT_TYPE = "SV"
LIABILITY_ACCOUNT_TYPE = "LB"
INVESTMENT_ACCOUNT_TYPE = "IV"

INCOME_TRANSACTION_TYPE = "inc"
EXPENSE_TRANSACTION_TYPE = "exp"
TRANSFER_IN_TRANSACTION_TYPE = "tranin"
TRANSFER_OUT_TRANSACTION_TYPE = "tranout"


ACCOUNT_TYPES_DICT = {
    CHECKING_ACCOUNT: "Checking",
    SAVING_ACCOUNT: "Savings",
    LIABILITIES_ACCOUNT: "Liability",
    INVESTMENT_ACCOUNT: "Investment"
}

ACCOUNT_TYPES = list(ACCOUNT_TYPES_DICT.keys())


EXPENSE_CATEGORY = "EXP"
INCOME_CATEGORY = "INC"

CATEGORY_TYPES_DICT = {
    EXPENSE_CATEGORY: "Expense",
    INCOME_CATEGORY: "Income"
}


class Account(BaseModel):
    id: Optional[str] = None
    name: str
    creation_date: datetime
    account_type: Literal["CH", "SV", "LB", "IV"]
    liquidity_type: Literal["low", "med", "high"] = HIGH_LIQUIDITY_TYPE
    is_active: bool = True
    balance: Decimal = Decimal("0.0")
    # TODO add is_archived
 

class Category(BaseModel):
    id: Optional[str] = None
    name: str
    parent_category_id: Optional[str] = None
    category_type: Literal["EXP", "INC"]


class Transaction(BaseModel):
    id: Optional[str] = None
    change: Decimal
    account_id: str
    category_id: Optional[str] = None
    transaction_type: Literal["inc", "exp", "tranin", "tranout", "div", "prof", "los"]
    description: Optional[str] = ""
    execution_date: date
    creation_date: datetime = None
    group_id: Optional[str] = None
