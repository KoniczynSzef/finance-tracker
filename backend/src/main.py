from auth.token_router import token_router
from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from src.database.config import get_session
from src.models.transaction import Transaction
from src.models.user import User  # type: ignore # noqa: F401 (imported but unused)

app = FastAPI()

app.include_router(token_router)


@app.get("/")
def health_check(session: Session = Depends(get_session)):
    return {"status": "ok"}


@app.get("/transactions")
def get_transactions(session: Session = Depends(get_session)):

    transactions = session.exec(select(Transaction)).all()

    return {"transactions": transactions}
