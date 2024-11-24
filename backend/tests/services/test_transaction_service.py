from decimal import Decimal

import pytest
from src.models.transaction import Transaction
from src.services.transaction_service import TransactionService

from tests.api_setup import database_setup, mock_session


@pytest.fixture(autouse=True)
def reset_mock_session():
    database_setup()


def test_transaction_service_init():
    """Test initialization of the TransactionService class."""
    transaction_service = TransactionService(session=mock_session())

    assert isinstance(transaction_service, TransactionService)


def test_get_transactions_empty_db():
    """Test get_transactions when there are no transactions in the database."""
    transaction_service = TransactionService(session=mock_session())

    transactions = transaction_service.get_transactions()

    assert transactions == []
    assert isinstance(transactions, list)


def test_get_transactions_with_data():
    """Test get_transactions when there are transactions in the database."""
    session = mock_session()
    transaction_service = TransactionService(session=session)

    # Add sample transactions to the session
    transaction1 = Transaction(amount=Decimal(
        100.0), description="Groceries", user_id=1)
    transaction2 = Transaction(amount=Decimal(
        200.0), description="Rent", user_id=1)

    session.add(transaction1)
    session.add(transaction2)
    session.commit()

    # Fetch transactions
    transactions = transaction_service.get_transactions()

    # Assert they were retrieved correctly
    assert len(transactions) == 2
    assert transactions[0].amount == 100.0
    assert transactions[0].description == "Groceries"
    assert transactions[1].amount == 200.0
    assert transactions[1].description == "Rent"
