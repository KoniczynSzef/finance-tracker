from database.config import get_session
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import StaticPool, create_engine
from sqlmodel import Session, SQLModel

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, echo=True, connect_args={
                       "check_same_thread": False}, poolclass=StaticPool)


def override_get_session():
    session = Session(engine)

    try:
        return session

    finally:
        session.close()


app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)


def database_setup():
    SQLModel.metadata.create_all(engine)

    yield

    SQLModel.metadata.drop_all(engine)
