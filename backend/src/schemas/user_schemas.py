from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(default="")
    email: str = Field(default="")
    full_name: str = Field(default="")

    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)

    current_balance: Decimal = Field(default=Decimal(0.0))
    balance_threshold: Decimal = Field(default=Decimal(0.0))

    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())


class UserCreate(UserBase):
    password: str = Field(default="")


class UserRead(UserBase):
    id: int = Field()
    hashed_password: str = Field(default="")
