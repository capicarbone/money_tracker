from typing import List, Optional, Literal
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.types import String, Date, Float, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from money_tracker.models import Account, Category, Transaction


class Base(DeclarativeBase):
    pass


class MappedAccount(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    creation_date: Mapped[datetime] = mapped_column(Date)
    account_type: Mapped[Literal] = mapped_column(String(2))
    liquidity_type: Mapped[Literal] = mapped_column(String(4))
    is_active: Mapped[bool] = mapped_column(Boolean)
    balance: Mapped[Decimal] = mapped_column(Float(asdecimal=True))

    def to_object(self) -> Account:
        return Account(
            id=str(self.id),
            name=self.name,
            balance=self.balance.quantize(Decimal("0.00")),
            creation_date=self.creation_date,
            account_type=self.account_type,
            liquidity_type=self.liquidity_type,
        )


class MappedCategory(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    category_type: Mapped[Literal] = mapped_column(String(3))
    parent_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"))
    children: Mapped[List["MappedCategory"]] = relationship()

    def to_object(self) -> Category:
        return Category(
            id=str(self.id),
            name=self.name,
            category_type=self.category_type,
            parent_category_id=str(self.parent_category_id),
        )


class MappedTransaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    change: Mapped[Decimal] = mapped_column(Float(asdecimal=True))
    account_id: Mapped["MappedAccount"] = mapped_column(ForeignKey("account.id"))
    category_id: Mapped[Optional["MappedCategory"]] = mapped_column(
        ForeignKey("category.id")
    )
    transaction_type: Mapped[Literal] = mapped_column(String(7))
    description: Mapped[str] = mapped_column(String(250))
    execution_date: Mapped[date] = mapped_column(Date)
    creation_date: Mapped[datetime] = mapped_column(DateTime)
    group_id: Mapped[Optional[str]] = mapped_column(String(36))

    def to_object(self):
        return Transaction(
            id=str(self.id),
            change=self.change,
            account_id=str(self.account_id),
            category_id=str(self.category_id),
            transaction_type=self.transaction_type,
            description=self.description,
            execution_date=self.execution_date,
            creation_date=self.creation_date,
            group_id=self.group_id,
        )
