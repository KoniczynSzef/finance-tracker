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


def test_get_transactions_by_category(transaction_service: TransactionService):
    """Test the function exists."""

    # The function should exist.
    assert callable(transaction_service.get_transactions_by_category)


def test_get_transactions_by_category_with_no_transactions(transaction_service: TransactionService):
    """Test getting transactions by category with no transactions."""
    response = transaction_service.get_transactions_by_category(1, "Income")

    # There should be no transactions.
    assert len(response) == 0


def test_get_transactions_by_category_with_one_transaction(transaction_service: TransactionService):
    """Test getting transactions by category with one transaction."""
    user = User(id=1, email="test@test.com", full_name="Test User")

    session = mock_session()

    session.add(Transaction(id=1, user_id=1,
                name="Test Transaction", amount=Decimal(100), category="Income"))
    session.add(user)
    session.commit()

    response = transaction_service.get_transactions_by_category(1, "Income")

    # There should be one transaction.
    assert len(response) == 1
    assert response[0].name == "Test Transaction"


def test_get_transactions_by_category_with_many_different_transactions(transaction_service: TransactionService):
    """Test getting transactions by category with many transactions."""
    user = User(id=1, email="test@test.com", full_name="Test User")

    session = mock_session()
    session.add(Transaction(id=1, user_id=1,
                name="Test Transaction", amount=Decimal(100), category="Income"))
    session.add(Transaction(id=2, user_id=1,
                name="Test Transaction 2", amount=Decimal(200), category="Expenses"))
    session.add(user)
    session.commit()

    response = transaction_service.get_transactions_by_category(1, "Income")

    # There should be one transaction.
    assert len(response) == 1
    assert response[0].name == "Test Transaction"


def test_get_transactions_by_category_with_many_transactions(transaction_service: TransactionService):
    """Test getting transactions by category with many transactions and different category."""
    user = User(id=1, email="test@test.com", full_name="Test User")

    session = mock_session()
    session.add(Transaction(id=1, user_id=1,
                name="Test Transaction", amount=Decimal(100), category="Income"))
    session.add(Transaction(id=2, user_id=1,
                name="Test Transaction 2", amount=Decimal(200), category="Income"))
    session.add(user)
    session.commit()

    response = transaction_service.get_transactions_by_category(1, "Income")

    # There should be two transactions.
    assert len(response) == 2
    assert response[0].name == "Test Transaction"
    assert response[1].name == "Test Transaction 2"
