from decimal import Decimal

from models.transaction import Transaction
from src.models.user import User


def test_user():
    user = User(username="test", email="test@test.com", full_name="Test User")

    assert user is not None


def test_user_default_values():
    user = User(id=1, username="test",
                email="test@test.com", full_name="Test User")

    assert user.id is not None
    assert user.username == "test"
    assert user.email == "test@test.com"
    assert user.full_name == "Test User"

    assert user.current_balance == Decimal(0.0)
    assert user.balance_threshold == Decimal(0.0)
    assert user.is_verified is False
    assert user.is_active is True

    assert user.created_at is not None
    assert user.updated_at is not None

    assert user.transactions == []


def test_user_with_values():
    user = User(id=1, username="test", email="test@test.com", full_name="Test User",
                current_balance=Decimal(100), balance_threshold=Decimal(50), is_verified=True, is_active=False)

    assert user.id == 1
    assert user.username == "test"
    assert user.email == "test@test.com"
    assert user.full_name == "Test User"

    assert user.current_balance == Decimal(100)
    assert user.balance_threshold == Decimal(50)
    assert user.is_verified is True
    assert user.is_active is False

    assert user.created_at is not None
    assert user.updated_at is not None

    assert user.transactions == []


def test_user_with_transactions():
    user = User(username="test", email="test@test.com", full_name="Test User",
                current_balance=Decimal(100), balance_threshold=Decimal(50), is_verified=True, is_active=False)

    user.id = 1

    transaction = Transaction(name="test", amount=Decimal(
        100), user_id=user.id, user=user)

    user.transactions.append(transaction)

    assert user.transactions == [transaction]
