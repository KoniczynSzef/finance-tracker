from decimal import Decimal

import pytest
from services.transaction_service import TransactionService
from sqlmodel import select
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


def test_add_transaction(transaction_service: TransactionService):
    """Test the function exists."""

    assert callable(transaction_service.add_transaction)


def test_add_transaction_with_invalid_amount(transaction_service: TransactionService):
    """Test adding a transaction with an invalid amount."""
    user = User(id=1, email="test@test.com", full_name="Test User")
    user.id = 1

    # The amount should be required to add a transaction.
    with pytest.raises(ValueError):
        transaction_service.add_transaction(
            Transaction(user_id=user.id, user=user, name="Test Transaction", amount=Decimal(0)), user)


def test_add_transaction_with_valid_amount(transaction_service: TransactionService):
    """Test adding a transaction with a valid amount."""
    user = User(id=1, email="test@test.com", full_name="Test User")
    user.id = 1

    transaction = transaction_service.add_transaction(
        Transaction(user_id=user.id, user=user, name="Test Transaction", amount=Decimal(100)), user)

    # The transaction should have the correct amount.
    assert transaction.amount == Decimal(100)


def test_add_transaction_update_the_database(transaction_service: TransactionService):
    """Test adding a transaction updates the database."""
    user = User(id=1, email="test@test.com", full_name="Test User")
    user.id = 1

    created_transaction = transaction_service.add_transaction(
        Transaction(user_id=user.id, user=user, name="Test Transaction", amount=Decimal(100)), user)

    session = mock_session()
    transaction = session.exec(select(Transaction).where(
        Transaction.id == created_transaction.id)).first()

    # transaaction should exist in the database
    assert transaction is not None

    # The transaction should have the correct user ID and user object.
    assert transaction.user_id == user.id
    assert transaction.user == user


def test_add_transaction_with_invalid_user_id(transaction_service: TransactionService):
    """Test adding a transaction with an invalid user ID."""

    user = User(email="test@test.com", full_name="Test User")

    # The user ID should be required to add a transaction.
    with pytest.raises(ValueError):
        transaction_service.add_transaction(
            Transaction(user_id=0, user=user, name="Test Transaction", amount=Decimal(100)), user)


def test_add_transaction_with_valid_user_id(transaction_service: TransactionService):
    """Test adding a transaction with a valid user ID."""

    user = User(id=1, email="test@test.com", full_name="Test User")
    user.id = 1

    transaction = transaction_service.add_transaction(
        Transaction(user_id=user.id, user=user, name="Test Transaction", amount=Decimal(100)), user)

    # The transaction should have the correct user ID and user object.
    assert transaction.user_id == user.id
    assert transaction.user == user


def test_add_transaction_with_income(transaction_service: TransactionService):
    """Test adding a transaction with an income."""
    user = User(id=1, email="test@test.com", full_name="Test User")
    user.id = 1

    transaction = transaction_service.add_transaction(
        Transaction(user_id=user.id, user=user, name="Test Transaction", amount=Decimal(500), is_income=True), user)

    # The transaction should have the correct amount.
    assert transaction.amount == Decimal(500)


def test_add_transaction_with_outcome(transaction_service: TransactionService):
    """Test adding a transaction with an outcome."""
    user = User(id=1, email="test@test.com", full_name="Test User")
    user.id = 1

    transaction = transaction_service.add_transaction(
        Transaction(user_id=user.id, user=user, name="Test Transaction", amount=Decimal(100), is_income=False), user)

    # The transaction should have the correct amount.
    assert transaction.amount == Decimal(100)
