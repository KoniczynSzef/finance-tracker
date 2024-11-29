from decimal import Decimal

import pytest
from schemas.transaction_schemas import TransactionBase
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


def test_update_transaction_by_id(transaction_service: TransactionService):
    """Test the function exists."""
    assert callable(transaction_service.update_transaction_by_id)


def test_update_transaction_by_id_with_invalid_transaction_id(transaction_service: TransactionService):
    """Test the function returns None when the transaction id is invalid."""

    with pytest.raises(ValueError, match="Invalid transaction: Transaction does not exist."):
        transaction_service.update_transaction_by_id(0, 0, transaction=TransactionBase(
            name="Test Transaction", is_income=False, amount=Decimal(100)))


def test_update_transaction_by_id_with_invalid_user_id(transaction_service: TransactionService):
    """Test the function returns None when the user id is invalid."""

    with pytest.raises(ValueError, match="Invalid transaction: Transaction does not exist."):
        transaction_service.update_transaction_by_id(1, 0, transaction=TransactionBase(
            name="Test Transaction", is_income=False, amount=Decimal(100)))


def test_update_transaction_by_id_with_valid_transaction_id(transaction_service: TransactionService):
    """Test the function updates the transaction."""
    session = mock_session()

    session.add(User(id=1, username="Test User"))
    session.add(Transaction(id=1, name="Test Transaction",
                is_income=False, amount=Decimal(100), user_id=1))
    session.commit()

    transaction_service.update_transaction_by_id(1, 1, transaction=TransactionBase(
        name="Updated Transaction", is_income=False, amount=Decimal(200)))

    updated_transaction = session.exec(
        select(Transaction).where(Transaction.id == 1)).first()

    assert updated_transaction is not None
    assert updated_transaction.name == "Updated Transaction"
    assert updated_transaction.amount == Decimal(200)
