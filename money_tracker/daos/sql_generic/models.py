
from typing import List, Optional, Literal
from datetime import datetime
from sqlalchemy.types import String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from money_tracker.models import Account


class Base(DeclarativeBase):
    pass


class MappedAccount(Base):
    __tablename__='account'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    creation_date: Mapped[datetime] = mapped_column(Date)
    account_type: Mapped[Literal] = mapped_column(String(2))
    liquidity_type: Mapped[Literal] = mapped_column(String(4))

    def to_object(self) -> Account:
        return Account(
            id=str(self.id),
            name=self.name,
            creation_date=self.creation_date,
            account_type=self.account_type,
            liquidity_type=self.liquidity_type
        )
