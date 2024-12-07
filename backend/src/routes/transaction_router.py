from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from src.database.config import get_session
from src.models.user import User
from src.schemas.errors import (
    ACTION_ERROR,
    InvalidCredentials,
    NotFound,
    ValidationError,
)
from src.schemas.transaction_schemas import (
    TransactionBase,
    TransactionCreate,
    TransactionRead,
)
from src.services.auth_service import AuthService
from src.services.transaction_service import TransactionService
from src.utils.validate_current_user import validate_current_user

transaction_router = APIRouter(prefix="/transactions", tags=["transactions"])

auth_service = AuthService()


@transaction_router.get("/", response_model=list[TransactionRead], status_code=status.HTTP_200_OK)
def get_transactions(session: Session = Depends(get_session), user: User = Depends(auth_service.get_current_user)):
    validated_user_id = validate_current_user(user)
    transaction_service = TransactionService(session)

    return transaction_service.get_transactions_by_user_id(validated_user_id)


@transaction_router.get("/", response_model=list[TransactionRead], status_code=status.HTTP_200_OK)
def get_transactions_in_date_range(start_date: str, end_date: str, user: User = Depends(auth_service.get_current_user), session: Session = Depends(get_session)):
    return 0


@transaction_router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: TransactionCreate, user: User = Depends(auth_service.get_current_user), session: Session = Depends(get_session)):
    validate_current_user(user)
    transaction_service = TransactionService(session)

    try:
        created_transaction = transaction_service.add_transaction(
            user, transaction=transaction)

        transaction_service.update_user_balance(
            user, created_transaction.is_income, created_transaction.amount)
        return created_transaction
    except InvalidCredentials as e:
        raise ACTION_ERROR(e.args[0], status_code=status.HTTP_401_UNAUTHORIZED)
    except ValidationError as e:
        raise ACTION_ERROR(
            e.args[0], status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@transaction_router.put("/{transaction_id}", response_model=TransactionRead, status_code=status.HTTP_200_OK)
def update_transaction(transaction_id: int, transaction: TransactionBase, user: User = Depends(auth_service.get_current_user), session: Session = Depends(get_session)):
    validated_user_id = validate_current_user(user)
    transaction_service = TransactionService(session)

    try:
        updated_transaction = transaction_service.update_transaction_by_id(
            transaction_id=transaction_id, user_id=validated_user_id, transaction=transaction)

        transaction_service.update_user_balance(
            user=user, is_income=updated_transaction.is_income, amount=updated_transaction.amount)

        return updated_transaction
    except NotFound as e:
        raise ACTION_ERROR(e.args[0], status_code=status.HTTP_404_NOT_FOUND)
    except InvalidCredentials as e:
        raise ACTION_ERROR(e.args[0], status_code=status.HTTP_401_UNAUTHORIZED)


@transaction_router.delete("/{transaction_id}", response_model=TransactionRead, status_code=status.HTTP_200_OK)
def delete_transaction(transaction_id: int, user: User = Depends(auth_service.get_current_user), session: Session = Depends(get_session)):
    validated_user_id = validate_current_user(user)
    transaction_service = TransactionService(session)

    try:
        return transaction_service.delete_transaction_by_id(user_id=validated_user_id, transaction_id=transaction_id)
    except NotFound as e:
        raise ACTION_ERROR(e.args[0], status_code=status.HTTP_404_NOT_FOUND)
    except InvalidCredentials as e:
        raise ACTION_ERROR(e.args[0], status_code=status.HTTP_401_UNAUTHORIZED)


@transaction_router.delete("/all/{user_id}", response_model=str, status_code=status.HTTP_200_OK)
def delete_all_transaction(user: User = Depends(auth_service.get_current_user), session: Session = Depends(get_session)):
    validated_user_id = validate_current_user(user)
    transaction_service = TransactionService(session)

    return transaction_service.delete_all_transactions_by_user_id(user_id=validated_user_id)
