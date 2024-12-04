from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from src.database.config import get_session
from src.models.user import User
from src.schemas.user_schemas import UserCreate, UserRead
from src.services.auth_service import AuthService, credentials_exception
from src.utils.validate_current_user import validate_current_user

auth_router = APIRouter(prefix="/auth", tags=["auth"])

auth_service = AuthService()


@auth_router.get("/me")
def get_current_user(token: str, user: User = Depends(auth_service.get_current_user), session: Session = Depends(get_session)):
    validate_current_user(user)
    return auth_service.get_current_user(token, session)


@auth_router.post("/token")
def login_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_session)):
    auth_service = AuthService(session)

    try:
        return auth_service.login_user(form_data.username, form_data.password)
    except Exception:
        raise credentials_exception


@auth_router.post("/register", response_model=UserRead)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    auth_service = AuthService(session)

    try:
        return auth_service.register_user(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=e.args[0], headers={"WWW-Authenticate": "Bearer"})
