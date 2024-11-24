import pytest
from src.models.user import User  # type: ignore # noqa: F401
from src.services.transaction_service import TransactionService

from tests.api_setup import mock_database_create, mock_database_drop, mock_session


@pytest.fixture(autouse=True)
def setup():
    mock_database_create()

    yield

    mock_database_drop()


def test_transaction_service_init():
    """Test initialization of the TransactionService class."""
    transaction_service = TransactionService(session=mock_session())

    assert isinstance(transaction_service, TransactionService)


def test_transaction_service_init_with_custom_session():
    """Test initialization of the TransactionService class with a custom session."""
    session = mock_session()
    transaction_service = TransactionService(session=session)

    assert isinstance(transaction_service, TransactionService)
    assert transaction_service.session == session


def test_transaction_service_init_with_default_session():
    """Test initialization of the TransactionService class without a session."""
    transaction_service = TransactionService()

    assert isinstance(transaction_service, TransactionService)
    assert transaction_service.session is not None
