from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from sqlmodel import (
    Field,  # type: ignore
    Relationship,
    SQLModel,
)

from src.models.user import User


class TransactionRating(str, Enum):
    SATISFIED = "SATISFIED"
    NEUTRAL = "NEUTRAL"
    REGRETFUL = "REGRETFUL"
    DISLIKE = "DISLIKE"
    IMPORTANT = "IMPORTANT"


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default="")
    description: str = Field(default="")
    category: str = Field(default="General")
    is_income: bool = Field(default=False)
    amount: Decimal = Field(default=0.0)
    date: datetime = Field(default_factory=datetime.now)
    currency: str = Field(default="USD")
    tags: str = Field(default="")
    rating: TransactionRating = Field(default=TransactionRating.SATISFIED)

    is_recurring: bool = Field(default=False)
    recurrence_period_in_days: Optional[int] = Field(default=0)

    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    user_id: int = Field(foreign_key="user.id", nullable=False)
    user: "User" = Relationship(back_populates="transactions")
