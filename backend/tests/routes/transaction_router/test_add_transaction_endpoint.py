from decimal import Decimal
from os import getenv

import pytest
from database.config import get_session
from schemas.transaction_schemas import TransactionCreate
from src.models.user import User
from tests.api_setup import (
    client,
    mock_database_create,
    mock_database_drop,
)

session = get_session()


@pytest.fixture(autouse=True)
def setup():
    mock_database_create()
    user = User(username="Username Test", id=1)

    session.add(user)
    session.commit()
    session.refresh(user)

    yield

    mock_database_drop()


def test_post_transaction_endpoint_when_not_authenticated():
    # Assuming /transaction is the endpoint for posting
    payload = TransactionCreate(name="New Transaction", amount=Decimal(
        100), category="Test Category", user_id=1)

    response = client.post("/transactions", json=payload.model_dump_json())
    assert getenv("BACKEND_ENVIRONMENT") == "TEST"

    # Endpoint should return 401 if not authenticated
    assert response.status_code == 401

# TODO: WRITE TESTS FOR POST TRANSACTION ENDPOINT

# * WHEN AUTHENTICATED AND VALID PAYLOAD
# * WHEN AUTHENTICATED AND INVALID PAYLOAD
