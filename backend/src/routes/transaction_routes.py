from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from src.database.config import get_session
from src.models.user import User
from src.schemas.transaction_schemas import (
    TransactionCreate,
    TransactionRead,
)
from src.services.transaction_service import TransactionService

transaction_router = APIRouter(prefix="/transactions", tags=["transactions"])


@ transaction_router.get("/", response_model=list[TransactionRead])
def get_transactions(user_id: int, session: Session = Depends(get_session)):
    transaction_service = TransactionService(session)

    return transaction_service.get_transactions_by_user_id(user_id=user_id)


@transaction_router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction_by_id(user_id: int, transaction_id: int, session: Session = Depends(get_session)):
    transaction_service = TransactionService(session)

    try:
        return transaction_service.get_transaction_by_id(user_id=user_id, transaction_id=transaction_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=e.args[0], headers={"WWW-Authenticate": "Bearer"})


@ transaction_router.post("/", response_model=TransactionRead)
def create_transaction(user_id: int, transaction: TransactionCreate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found", headers={"WWW-Authenticate": "Bearer"})

    transaction_service = TransactionService(session)

    try:
        created_transaction = transaction_service.add_transaction(
            user, transaction=transaction)

        transaction_service.update_user_balance(
            user, created_transaction.is_income, created_transaction.amount)
        return created_transaction
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=e.args[0], headers={"WWW-Authenticate": "Bearer"})

# TODO: Implement update transaction endpoint


@ transaction_router.delete("/{transaction_id}", response_model=TransactionRead)
def delete_transaction(user_id: int, transaction_id: int, session: Session = Depends(get_session)):
    transaction_service = TransactionService(session)

    try:
        return transaction_service.delete_transaction_by_id(user_id=user_id, transaction_id=transaction_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=e.args[0], headers={"WWW-Authenticate": "Bearer"})


@ transaction_router.delete("/all/{user_id}", response_model=str)
def delete_all_transaction(user_id: int, transaction_id: int, session: Session = Depends(get_session)):
    transaction_service = TransactionService(session)
    return transaction_service.delete_all_transactions_by_user_id(user_id=user_id)
