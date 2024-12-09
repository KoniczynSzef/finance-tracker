from decimal import Decimal
from os import getenv

import pytest
from database.config import get_session
from schemas.auth_schemas import TokenData
from schemas.transaction_schemas import TransactionCreate
from services.auth_service import AuthService
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
    payload = TransactionCreate(name="New Transaction", amount=Decimal(
        100), category="Test Category", user_id=1)

    response = client.post("/transactions", json=payload.model_dump_json())
    assert getenv("BACKEND_ENVIRONMENT") == "TEST"

    # Endpoint should return 401 if not authenticated
    assert response.status_code == 401


def test_post_transaction_endpoint_when_authenticated():
    auth_service = AuthService(session)

    payload = TransactionCreate(name="New Transaction", amount=Decimal(
        100), category="Test Category", user_id=1)

    token = auth_service.create_access_token(
        TokenData(sub="Username Test", exp=60))
    auth_header = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/transactions", headers=auth_header, json=payload.model_dump_json())

    assert not response.text

    assert response.status_code == 201

# TODO: WRITE TESTS FOR POST TRANSACTION ENDPOINT

# * WHEN AUTHENTICATED AND VALID PAYLOAD
# * WHEN AUTHENTICATED AND INVALID PAYLOAD
