from datetime import datetime
from decimal import Decimal
from enum import Enum

# from models.transaction import TransactionRating
from pydantic import BaseModel, Field


class TransactionRating(str, Enum):
    SATISFIED = "SATISFIED"
    NEUTRAL = "NEUTRAL"
    REGRETFUL = "REGRETFUL"
    DISLIKE = "DISLIKE"
    IMPORTANT = "IMPORTANT"


class TransactionBase(BaseModel):
    name: str = Field(default="")
    description: str = Field(
        default="")
    category: str = Field(default="General")
    is_income: bool = Field(default=False)
    amount: Decimal = Field(..., gt=0,
                            description="Transaction amount must be greater than 0.")
    date: datetime = Field(default_factory=datetime.now)
    currency: str = Field(default="USD")
    tags: str = Field(default="")
    rating: TransactionRating = Field(
        default=TransactionRating.SATISFIED)

    is_recurring: bool = Field(default=False)
    recurrence_period_in_days: int = Field(default=0)


class TransactionCreate(TransactionBase):
    user_id: int = Field()


class TransactionRead(TransactionBase):
    id: int = Field()
    user_id: int = Field()

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TransactionsSummary(BaseModel):
    total_income: Decimal = Field(default=Decimal(0))
    total_expense: Decimal = Field(default=Decimal(0))
    total_transactions: int = Field(default=0)

    average_transaction_amount: Decimal = Field(default=Decimal(0))
    highest_transaction_amount: Decimal = Field(default=Decimal(0))
    lowest_transaction_amount: Decimal = Field(default=Decimal(0))
