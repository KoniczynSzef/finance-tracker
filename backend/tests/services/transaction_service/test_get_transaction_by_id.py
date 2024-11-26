from decimal import Decimal

import pytest
from services.transaction_service import TransactionService
from src.models.transaction import Transaction
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


@pytest.fixture
def user():
    return User(id=1, email="test@test.com", full_name="Test User")


def test_get_transaction_by_id(transaction_service: TransactionService, user: User):
    """Test the function exists."""
    assert callable(transaction_service.get_transaction_by_id)


def test_get_transaction_by_id_with_invalid_user_id(transaction_service: TransactionService, user: User):
    """Test getting a transaction with an invalid user ID."""
    user.id = None

    with pytest.raises(ValueError):
        transaction_service.get_transaction_by_id(user, 1)


def test_get_transaction_by_id_with_invalid_transaction_id(transaction_service: TransactionService, user: User):
    """Test getting a transaction with an invalid transaction ID."""
    user.id = 1

    with pytest.raises(ValueError):
        transaction_service.get_transaction_by_id(user, 1)


def test_get_transaction_by_id_with_valid_transaction_id(transaction_service: TransactionService, user: User):
    """Test getting a transaction with a valid transaction ID."""
    user.id = 1

    transaction = Transaction(
        user_id=user.id, user=user, name="Test Transaction", amount=Decimal(100))
    transaction.id = 1

    session = mock_session()
    session.add(transaction)
    session.commit()

    assert transaction_service.get_transaction_by_id(
        user, transaction.id) == transaction
