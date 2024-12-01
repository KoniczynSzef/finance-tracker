from decimal import Decimal

import pytest
from services.transaction_service import TransactionService
from src.models.transaction import Transaction
from src.models.user import User
from src.schemas.errors import InvalidCredentials, NotFound
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


def test_get_transaction_by_id_that_does_not_exist(transaction_service: TransactionService):
    """Test getting a transaction that does not exist."""

    with pytest.raises(NotFound, match="Invalid transaction: Transaction does not exist."):
        transaction_service.get_transaction_by_id(0, 1)


def test_get_transaction_by_id_when_user_does_not_own_transaction(transaction_service: TransactionService, user: User):
    """Test getting a transaction when the user does not own the transaction."""
    user.id = 2

    transaction = Transaction(id=1,
                              user_id=1, name="Test Transaction", amount=Decimal(100))
    transaction.id = 1

    session = mock_session()
    session.add(transaction)
    session.commit()

    with pytest.raises(InvalidCredentials, match="Invalid transaction: User does not own the transaction."):
        transaction_service.get_transaction_by_id(transaction.id, user.id)


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
        transaction.id, user.id) == transaction
