
from decimal import Decimal
from os import getenv

import pytest
from database.config import get_session
from schemas.auth_schemas import TokenData
from services.auth_service import AuthService
from src.models.transaction import Transaction
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
    user = User(username="Username Test")

    session.add(user)
    session.commit()
    session.refresh(user)

    yield

    mock_database_drop()


def test_get_transactions_endpoint_when_not_authenticated():
    response = client.get("/transactions")
    assert getenv("BACKEND_ENVIRONMENT") == "TEST"

    # Endpoint should return 401 if not authenticated
    assert response.status_code == 401


def test_get_transactions_endpoint_when_authenticated():
    auth_service = AuthService(session)

    token = auth_service.create_access_token(
        TokenData(sub="Username Test", exp=60))
    auth_header = {"Authorization": f"Bearer {token}"}

    response = client.get("/transactions", headers=auth_header)

    assert response.status_code == 200


def test_get_transactions_endpoint_when_authenticated_and_no_transactions():
    auth_service = AuthService(session)

    token = auth_service.create_access_token(
        TokenData(sub="Username Test", exp=60))
    auth_header = {"Authorization": f"Bearer {token}"}

    response = client.get("/transactions", headers=auth_header)
    assert response.json() == []


def test_get_transactions_endpoint_when_authenticated_and_transaction():
    auth_service = AuthService(session)

    transaction = Transaction(
        id=1, name="Transaction 1", amount=Decimal(100), user_id=1)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    token = auth_service.create_access_token(
        TokenData(sub="Username Test", exp=60))

    auth_header = {"Authorization": f"Bearer {token}"}
    response = client.get("/transactions", headers=auth_header)

    assert len(response.json()) == 1

    assert response.json()[0]["id"] == 1
    assert response.json()[0]["name"] == "Transaction 1"
    assert Decimal(response.json()[0]["amount"]) == Decimal(100)


def test_get_transactions_endpoint_when_authenticated_and_transactions():
    auth_service = AuthService(session)

    transaction = Transaction(
        id=1, name="Transaction 1", amount=Decimal(100), user_id=1)

    second_transaction = Transaction(
        id=2, name="Transaction 2", amount=Decimal(200), user_id=1)

    session.add(transaction)
    session.add(second_transaction)
    session.commit()
    session.refresh(transaction)
    session.refresh(second_transaction)

    token = auth_service.create_access_token(
        TokenData(sub="Username Test", exp=60))

    auth_header = {"Authorization": f"Bearer {token}"}
    response = client.get("/transactions", headers=auth_header)

    assert len(response.json()) == 2

    assert response.json()[0]["id"] == 1
    assert response.json()[0]["name"] == "Transaction 1"
    assert Decimal(response.json()[0]["amount"]) == Decimal(100)

    assert response.json()[1]["id"] == 2
    assert response.json()[1]["name"] == "Transaction 2"
    assert Decimal(response.json()[1]["amount"]) == Decimal(200)
