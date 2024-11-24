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


@app.get("/transactions/{user_id}")
def get_transactions(user_id: int, session: Session = Depends(get_session)):
    transaction_service = TransactionService(session)
    transactions = transaction_service.get_transactions_by_user_id(user_id)

    return {"transactions": transactions}
