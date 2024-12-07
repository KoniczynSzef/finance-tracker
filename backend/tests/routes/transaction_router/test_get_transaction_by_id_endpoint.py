# from decimal import Decimal
# from os import getenv

# import pytest
# from database.config import get_session
# from schemas.auth_schemas import TokenData
# from services.auth_service import AuthService
# from src.models.transaction import Transaction
# from src.models.user import User
# from tests.api_setup import (
#     client,
#     mock_database_create,
#     mock_database_drop,
# )

# session = get_session()


# @pytest.fixture(autouse=True)
# def setup():
#     mock_database_create()
#     user = User(username="Username Test")

#     session.add(user)
#     session.commit()
#     session.refresh(user)

#     yield

#     mock_database_drop()


# def test_get_transaction_by_id_endpoint_when_not_authenticated():
#     # Assuming /transactions/{transaction_id} is the endpoint
#     response = client.get("/transactions/1")
#     assert getenv("BACKEND_ENVIRONMENT") == "TEST"

#     # Endpoint should return 401 if not authenticated
#     assert response.status_code == 401


# def test_get_transaction_by_id_endpoint_when_authenticated_and_transaction_exists():
#     auth_service = AuthService(session)

#     # Create a transaction in the test database
#     transaction = Transaction(
#         id=1, name="Transaction 1", amount=Decimal(100), user_id=1
#     )
#     session.add(transaction)
#     session.commit()
#     session.refresh(transaction)

#     # Create an access token for the test user
#     token = auth_service.create_access_token(
#         TokenData(sub="Username Test", exp=60)
#     )
#     auth_header = {"Authorization": f"Bearer {token}"}

#     # Call the endpoint
#     response = client.get(
#         f"/transactions/{transaction.id}", headers=auth_header)

#     # Validate response
#     assert response.status_code == 200
#     response_data = response.json()

#     assert response_data["id"] == transaction.id
#     assert response_data["name"] == transaction.name
#     assert Decimal(response_data["amount"]) == transaction.amount


# def test_get_transaction_by_id_endpoint_when_authenticated_and_transaction_does_not_exist():
#     auth_service = AuthService(session)

#     # Create an access token for the test user
#     token = auth_service.create_access_token(
#         TokenData(sub="Username Test", exp=60)
#     )
#     auth_header = {"Authorization": f"Bearer {token}"}

#     # Call the endpoint with a non-existent transaction ID
#     response = client.get("/transactions/999", headers=auth_header)

#     # Validate response
#     # Assuming the endpoint returns a 404 for non-existent transactions
#     assert response.status_code == 404
#     assert response.json()[
#         "detail"] == "Invalid transaction: Transaction does not exist."
