from database.config import get_session
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import StaticPool, create_engine
from sqlmodel import Session, SQLModel

DATABASE_URL = "sqlite:///:memory:"

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
