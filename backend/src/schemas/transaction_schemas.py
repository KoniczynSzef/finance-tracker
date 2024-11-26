from datetime import datetime
from decimal import Decimal

from models.transaction import TransactionRating
from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    name: str = Field(default="")
    description: str = Field(
        default="")
    category: str = Field(default="General")
    is_income: bool = Field(default=False)
    amount: Decimal = Field(..., gt=0)
    date: datetime = Field(default_factory=datetime.now)
    currency: str = Field(default="USD")
    tags: str = Field(default="")
    rating: TransactionRating = Field(
        default=TransactionRating.SATISFIED)

    is_recurring: bool = Field(default=False)
    recurrence_period_in_days: int = Field(default=0)


class TransactionCreate(TransactionBase):
    user_id: int = Field(default=0)


class TransactionUpdate(TransactionBase):
    # TODO: add every field as optional
    pass


class TransactionRead(TransactionBase):
    id: int = Field(default=0)
    user_id: int = Field(default=0)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
