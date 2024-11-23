from os import getenv

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set!")

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    session = Session(engine)

    try:
        return session
    finally:
        session.close()