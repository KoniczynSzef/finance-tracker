from datetime import datetime
from decimal import Decimal
from typing import Optional

from models.transaction import Transaction
from sqlmodel import (
    Field,  # type: ignore
    Relationship,
    SQLModel,
)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(default="", unique=True, index=True)
    email: str = Field(default="", unique=True, index=True)
    full_name: str = Field(default="")
    hashed_password: str = Field(default="")

    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)

    current_balance: Decimal = Field(default=Decimal(0.0))
    balance_threshold: Decimal = Field(default=Decimal(0.0))

    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    transactions: list[Transaction] = Relationship(back_populates="user")
