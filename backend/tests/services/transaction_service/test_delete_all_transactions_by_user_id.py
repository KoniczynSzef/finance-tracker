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


def test_delete_all_transactions_by_user_id(transaction_service: TransactionService):
    """Test the function exists."""

    assert callable(transaction_service.delete_all_transactions_by_user_id)


def test_delete_all_transactions_by_user_id_with_no_transactions(transaction_service: TransactionService):
    """Test deleting all transactions by user ID with no transactions."""
    response = transaction_service.delete_all_transactions_by_user_id(1)

    assert response == "No transactions to delete."


def test_delete_all_transactions_by_user_id_with_one_transaction(transaction_service: TransactionService):
    """Test deleting all transactions by user ID with transactions."""
    user = User(id=1, email="test@test.com", full_name="Test User")

    session = mock_session()

    session.add(Transaction(id=1, user_id=1,
                name="Test Transaction", amount=Decimal(100)))
    session.add(user)
    session.commit()

    response = transaction_service.delete_all_transactions_by_user_id(1)

    assert response == "Transactions deleted successfully."
    assert len(session.exec(select(Transaction)).all()) == 0


def test_delete_all_transactions_by_user_id_with_many_transactions(transaction_service: TransactionService):
    """Test deleting all transactions by user ID with many transactions."""
    user = User(id=1, email="test@test.com", full_name="Test User")

    session = mock_session()

    session.add(Transaction(id=1, user_id=1,
                name="Test Transaction", amount=Decimal(100)))
    session.add(Transaction(id=2, user_id=1,
                name="Test Transaction 2", amount=Decimal(200)))
    session.add(user)
    session.commit()

    response = transaction_service.delete_all_transactions_by_user_id(1)

    assert response == "Transactions deleted successfully."
    assert len(session.exec(select(Transaction)).all()) == 0
