from uuid import UUID
from typing import Literal, Optional
from decimal import Decimal

from datetime import datetime, date
from pydantic import BaseModel

CHECKING_ACCOUNT = 'CH'
SAVING_ACCOUNT = 'SV'
LIABILITIES_ACCOUNT = 'LB'
INVESTMENT_ACCOUNT = 'IV'

HIGH_LIQUIDITY_TYPE = 'high'

CHECKING_ACCOUNT_TYPE = 'CH'
SAVINGS_ACCOUNT_TYPE = 'SV'
LIABILITY_ACCOUNT_TYPE = 'LB'
INVESTMENT_ACCOUNT_TYPE = 'IV'

ACCOUNT_TYPES = [
    CHECKING_ACCOUNT_TYPE,
    SAVINGS_ACCOUNT_TYPE,
    LIABILITY_ACCOUNT_TYPE,
    INVESTMENT_ACCOUNT_TYPE
]

class Account(BaseModel):
    id: Optional[str] = None
    name: str
    creation_date: datetime    
    account_type: Literal['CH', 'SV', 'LB', 'IV']
    liquidity_type: Literal['low', 'med', 'high'] = HIGH_LIQUIDITY_TYPE


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
