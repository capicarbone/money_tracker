from uuid import UUID
from typing import Literal, Optional
from decimal import Decimal

from datetime import datetime, date
from pydantic import BaseModel

CHECKING_ACCOUNT = 'CH'
SAVING_ACCOUNT = 'SV'
LIABILITIES_ACCOUNT = 'LB'
INVESTMENT_ACCOUNT = 'IV'

class Account(BaseModel):
    id: Optional[str]
    name: str
    creation_date: datetime
    account_type: Literal['CH', 'SV', 'LB', 'IV']
    liquidity_type: Literal['low', 'med', 'high']


EXPENSE_CATEGORY = 'exp'
INCOME_CATEGORY = 'inc'

class Category(BaseModel):
    id: Optional[str] = None
    name: str
    parent_category_id: Optional[str] = None
    category_type: Literal['exp', 'inc']

class Transaction(BaseModel):
    id: Optional[str]
    change: Decimal
    account_id: str
    category_id: Optional[str]
    transaction_type: Literal['inc', 'exp', 'tran', 'div', 'prof', 'los']
    description: Optional[str]
    execution_date: date
    creation_date: datetime
    group_id: UUID
