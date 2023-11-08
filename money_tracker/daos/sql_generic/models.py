
from typing import List, Optional, Literal
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.types import String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from money_tracker.models import Account, Category


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

class MappedCategory(Base):
    __tablename__='category'

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
            parent_category_id=str(self.parent_category_id)
        )
    

    