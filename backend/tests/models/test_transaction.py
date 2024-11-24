from decimal import Decimal

from src.models.transaction import Transaction
from src.models.user import (
    User,  # type: ignore # noqa: F401 (imported because if not, transaction does not find User class)
)


def test_transaction():
    transaction = Transaction(name="test", amount=Decimal(100), user_id=1)

    assert transaction is not None


def test_transaction_default_values():
    transaction = Transaction(
        id=1, name="test", amount=Decimal(100), user_id=1)

    assert transaction.id is not None
    assert transaction.name == "test"
    assert transaction.description == ""
    assert transaction.currency == "USD"
    assert transaction.is_income is False
    assert transaction.is_recurring is False
    assert transaction.recurrence_period_in_days == 0
    assert transaction.amount == Decimal(100)
    assert transaction.created_at is not None
    assert transaction.updated_at is not None

    assert transaction.user_id == 1


def test_transaction_with_values():
    transaction = Transaction(
        id=1, name="test", amount=Decimal(100), user_id=1, description="test description", currency="EUR", is_income=True, is_recurring=True, recurrence_period_in_days=7)

    assert transaction.id == 1
    assert transaction.name == "test"
    assert transaction.description == "test description"
    assert transaction.currency == "EUR"
    assert transaction.is_income is True
    assert transaction.is_recurring is True
    assert transaction.recurrence_period_in_days == 7
    assert transaction.amount == Decimal(100)
    assert transaction.created_at is not None
    assert transaction.updated_at is not None


def test_transaction_with_user():
    user = User(username="test", email="test@test.com", full_name="Test User")

    user.id = 1

    transaction = Transaction(name="test", amount=Decimal(
        100), user_id=user.id, user=user)

    assert transaction.user_id == 1
    assert transaction.user == user
