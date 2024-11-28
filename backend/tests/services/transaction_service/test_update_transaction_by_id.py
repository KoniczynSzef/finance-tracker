from decimal import Decimal

import pytest
from schemas.transaction_schemas import TransactionUpdate
from services.transaction_service import TransactionService
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
        transaction_service.update_transaction_by_id(0, 0, transaction=TransactionUpdate(
            id=0, name="Test Transaction", is_income=False, amount=Decimal(100), user_id=1))


# TODO: TESTS FOR INVALID USER ID AND ACTUAL UPDATE IN THE DATABASE
