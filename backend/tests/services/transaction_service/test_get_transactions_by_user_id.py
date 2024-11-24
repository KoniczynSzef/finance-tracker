from decimal import Decimal

import pytest
from src.models.transaction import Transaction
from src.models.user import User
from src.services.transaction_service import TransactionService

from tests.api_setup import (
    mock_database_create,
    mock_database_drop,
    mock_session,
)


@pytest.fixture(autouse=True)
def setup():
    mock_database_create()

    yield

    mock_database_drop()


@pytest.fixture
def transaction_service():
    return TransactionService(session=mock_session())


def test_get_transactions_by_random_user_id(transaction_service: TransactionService):
    """Test getting transactions by a random user ID."""

    transactions = transaction_service.get_transactions_by_user_id(1)

    # No transactions should be returned for a random user ID.
    assert transactions == []


def test_get_transactions_by_user_with_no_transactions(transaction_service: TransactionService):
    """Test getting transactions by user ID when the user has no transactions."""

    user = User(id=2, email="user2@test.com", full_name="User Two")
    user.id = 2

    transactions = transaction_service.get_transactions_by_user_id(user.id)

    # No transactions should be returned for this user.
    assert transactions == []


def test_get_transactions_by_user_id(transaction_service: TransactionService):
    user = User(id=1, email="test@test.com", full_name="Test User")
    user.id = 1

    transaction = Transaction(
        id=1, user_id=user.id, user=user, name="Test Transaction", amount=Decimal(100), is_income=True)

    session = mock_session()

    session.add(transaction)
    session.commit()

    transactions = transaction_service.get_transactions_by_user_id(user.id)

    # Only one transaction should be returned for this user. The transaction id should match the one we added.
    assert len(transactions) == 1
    assert transactions[0].id == transaction.id


def test_get_multiple_transactions_by_user_id(transaction_service: TransactionService):
    """Test getting multiple transactions by user ID."""

    user = User(id=3, email="user3@test.com", full_name="User Three")
    user.id = 3

    transaction1 = Transaction(id=1, user_id=user.id, user=user,
                               name="First Transaction", amount=Decimal(100), is_income=True)
    transaction2 = Transaction(id=2, user_id=user.id, user=user,
                               name="Second Transaction", amount=Decimal(50), is_income=False)

    session = mock_session()

    session.add(transaction1)
    session.add(transaction2)
    session.commit()

    transactions = transaction_service.get_transactions_by_user_id(user.id)

    # Only two transactions should be returned for this user. The transaction ids should match the ones we added.
    assert len(transactions) == 2
    assert transactions[0].id == transaction1.id
    assert transactions[1].id == transaction2.id


def test_get_transactions_order(transaction_service: TransactionService):
    """Test that transactions are returned in the correct order."""

    user = User(id=4, email="user4@test.com", full_name="User Four")
    user.id = 4

    transaction1 = Transaction(id=1, user_id=user.id, user=user,
                               name="First Transaction", amount=Decimal(100), is_income=True)
    transaction2 = Transaction(id=2, user_id=user.id, user=user,
                               name="Second Transaction", amount=Decimal(50), is_income=False)

    session = mock_session()

    session.add(transaction1)
    session.add(transaction2)
    session.commit()

    transactions = transaction_service.get_transactions_by_user_id(user.id)

    # Assuming the order should be by ID or timestamp; adjust as needed
    assert transactions[0].id is not None
    assert transactions[1].id is not None
    assert transactions[0].id < transactions[1].id
