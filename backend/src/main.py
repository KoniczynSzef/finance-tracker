from fastapi import Depends, FastAPI
from sqlmodel import Session

from src.auth.token_router import token_router
from src.database.config import get_session
from src.services.transaction_service import TransactionService

app = FastAPI()

app.include_router(token_router)


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.get("/transactions")
def get_transactions(session: Session = Depends(get_session)):
    transaction_service = TransactionService(session)
    transactions = transaction_service.get_transactions()

    return {"transactions": transactions}
