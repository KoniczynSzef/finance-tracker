import os

from database.config import get_session
from fastapi.testclient import TestClient
from main import app
from schemas.auth_schemas import TokenData
from services.auth_service import AuthService
from sqlalchemy import StaticPool, create_engine
from sqlmodel import Session, SQLModel

DATABASE_URL = "sqlite:///:memory:"
os.environ["BACKEND_ENVIRONMENT"] = "TEST"

mock_engine = create_engine(DATABASE_URL, echo=True, connect_args={
    "check_same_thread": False}, poolclass=StaticPool)


def mock_session():
    session = Session(mock_engine)

    try:
        return session

    finally:
        session.close()


app.dependency_overrides[get_session] = mock_session

client = TestClient(app)


def mock_database_create():
    SQLModel.metadata.create_all(mock_engine)


def mock_database_drop():
    SQLModel.metadata.drop_all(mock_engine)


def unauthenticated_client():
    return TestClient(app)


def authenticated_client(client: TestClient):
    auth_service = AuthService()

    token = auth_service.create_access_token(TokenData(sub="test", exp=100))
    client.headers.update({"Authorization": f"Bearer {token}"})

    return client
