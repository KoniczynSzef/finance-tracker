from decimal import Decimal
from os import getenv
from typing import Any

import pytest
from database.config import get_session
from schemas.auth_schemas import TokenData
from schemas.transaction_schemas import TransactionCreate
from services.auth_service import AuthService
from sqlmodel import select
from src.models.transaction import Transaction
from src.models.user import User
from tests.api_setup import (
    client,
    mock_database_create,
    mock_database_drop,
)
from tests.serialize_payload import serialize_payload

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

    payload_dict = serialize_payload(payload.model_dump())

    token = auth_service.create_access_token(
        TokenData(sub="Username Test", exp=60))
    auth_header = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/transactions", headers=auth_header, json=payload_dict)

    # Endpoint should return 201 if authenticated
    assert response.status_code == 201


def test_post_transaction_endpoint_properly_updates_database():
    auth_service = AuthService(session)

    payload = TransactionCreate(name="New Transaction", amount=Decimal(
        100), category="Test Category", user_id=1)

    payload_dict = serialize_payload(payload.model_dump())

    token = auth_service.create_access_token(
        TokenData(sub="Username Test", exp=60))
    auth_header = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/transactions", headers=auth_header, json=payload_dict)

    data: dict[str, Any] = response.json()

    transaction = session.exec(select(Transaction).where(
        Transaction.name == data["name"])).first()

    # Transaction should be created
    assert transaction is not None
    assert transaction.name == "New Transaction"
    assert transaction.amount == Decimal(100)
    assert transaction.category == "Test Category"
