from datetime import datetime, timedelta
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


def test_get_transactions_in_date_range(transaction_service: TransactionService):
    """Test the function exists."""

    # The function should exist.
    assert callable(transaction_service.get_transactions_in_date_range)


def test_get_transactions_in_date_range_with_no_transactions(transaction_service: TransactionService):
    """Test getting transactions in date range with no transactions."""
    response = transaction_service.get_transactions_in_date_range(
        1, datetime.now(), datetime.now())

    # There should be no transactions.
    assert len(response) == 0


def test_get_transactions_in_date_range_with_one_transaction(transaction_service: TransactionService):
    """Test getting transactions in date range with one transaction."""
    user = User(id=1, email="test@test.com", full_name="Test User")

    session = mock_session()

    session.add(Transaction(id=1, user_id=1,
                name="Test Transaction", amount=Decimal(100), date=datetime.now()))
    session.add(user)
    session.commit()

    response = transaction_service.get_transactions_in_date_range(
        1, datetime.now() - timedelta(days=1), datetime.now())

    # There should be one transaction.
    assert len(response) == 1
    assert response[0].name == "Test Transaction"


def test_get_transactions_in_date_range_with_many_transactions(transaction_service: TransactionService):
    """Test getting transactions in date range with many transactions."""
    user = User(id=1, email="test@test.com", full_name="Test User")

    session = mock_session()

    session.add(Transaction(id=1, user_id=1,
                name="Test Transaction", amount=Decimal(100), date=datetime.now()))
    session.add(Transaction(id=2, user_id=1,
                name="Test Transaction 2", amount=Decimal(200), date=datetime.now()))

    session.add(user)
    session.commit()

    response = transaction_service.get_transactions_in_date_range(
        1, datetime.now() - timedelta(days=1), datetime.now())

    # There should be two transactions.
    assert len(response) == 2
    assert response[0].name == "Test Transaction"
    assert response[1].name == "Test Transaction 2"


def test_get_transactions_in_date_range_with_many_transactions_and_different_dates(transaction_service: TransactionService):
    """Test getting transactions in date range with many transactions and different dates."""
    user = User(id=1, email="test@test.com", full_name="Test User")

    session = mock_session()
    session.add(Transaction(id=1, user_id=1,
                name="Test Transaction", amount=Decimal(100), date=datetime.now()))
    session.add(Transaction(id=2, user_id=1,
                # Older transaction
                            name="Test Transaction 2", amount=Decimal(200), date=datetime.now() - timedelta(days=1)))

    session.add(user)
    session.commit()

    response = transaction_service.get_transactions_in_date_range(
        1, datetime.now() - timedelta(days=2), datetime.now() - timedelta(days=1))

    # There should be one transaction.
    assert len(response) == 1
    assert response[0].name == "Test Transaction 2"
