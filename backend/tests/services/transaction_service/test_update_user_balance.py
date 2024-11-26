from decimal import Decimal

import pytest
from services.transaction_service import TransactionService
from src.models.user import User

from tests.api_setup import mock_database_create, mock_database_drop, mock_session


@pytest.fixture(autouse=True)
def setup():
    mock_database_create()

    yield

    mock_database_drop()


@pytest.fixture
def transaction_service():
    return TransactionService(session=mock_session())


def test_update_user_balance(transaction_service: TransactionService):
    """Test the function exists."""
    assert callable(transaction_service.update_user_balance)


def test_update_user_balance_with_invalid_user_id(transaction_service: TransactionService):
    """Test updating a user balance with an invalid user ID."""
    user = User(id=1, email="test@test.com", full_name="Test User")
    user.id = None

    # The user ID should be required to update a user balance.
    with pytest.raises(ValueError):
        transaction_service.update_user_balance(
            user, is_income=True, amount=Decimal(100))


def test_update_user_balance_with_invalid_amount(transaction_service: TransactionService):
    """Test updating a user balance with an invalid amount."""
    user = User(id=1, email="test@test.com", full_name="Test User")
    user.id = 1

    # The amount should be required to update a user balance.
    with pytest.raises(ValueError):
        transaction_service.update_user_balance(
            user, is_income=False, amount=Decimal(0))

    with pytest.raises(ValueError):
        transaction_service.update_user_balance(
            user, is_income=False, amount=Decimal(-100))


def test_update_user_balance_with_valid_amount(transaction_service: TransactionService):
    """Test updating a user balance with a valid amount."""
    user = User(id=1, email="test@test.com", full_name="Test User")
    user.id = 1

    transaction_service.update_user_balance(
        user, is_income=True, amount=Decimal(100))

    # The user balance should have been updated.
    assert user.current_balance == Decimal(100)


def test_update_user_balance_with_income(transaction_service: TransactionService):
    """Test updating a user balance with an income."""
    user = User(id=1, email="test@test.com",
                full_name="Test User", current_balance=Decimal(0))
    user.id = 1

    transaction_service.update_user_balance(
        user, is_income=True, amount=Decimal(500))

    # The user balance should have been updated.
    assert user.current_balance == Decimal(500)


def test_update_user_balance_with_outcome(transaction_service: TransactionService):
    """Test updating a user balance with an outcome."""
    user = User(id=1, email="test@test.com",
                full_name="Test User", current_balance=Decimal(0))
    user.id = 1

    transaction_service.update_user_balance(
        user, is_income=False, amount=Decimal(100))

    # The user balance should have been updated to -100.
    assert user.current_balance == Decimal(-100)


def test_update_user_balance_with_income_and_outcome(transaction_service: TransactionService):
    """Test updating a user balance with an income and outcome."""
    user = User(id=1, email="test@test.com",
                full_name="Test User", current_balance=Decimal(0))
    user.id = 1

    transaction_service.update_user_balance(
        user, is_income=True, amount=Decimal(500))
    transaction_service.update_user_balance(
        user, is_income=False, amount=Decimal(100))

    # The user balance should have been updated to 400.
    assert user.current_balance == Decimal(400)
