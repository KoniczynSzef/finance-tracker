from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.database.config import get_session
from src.schemas.auth_schemas import Token, TokenData
from src.services.auth_service import AuthService, credentials_exception

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/current_user")
def get_current_user(token: str, session: Session = Depends(get_session)):
    auth_service = AuthService(session)

    return auth_service.get_current_user(token)


@auth_router.post("/token")
def create_access_token(token_data: TokenData, session: Session = Depends(get_session)):
    auth_service = AuthService(session)

    return auth_service.create_access_token(token_data)


@auth_router.post("/login", response_model=Token)
def login_user(username: str, password: str, session: Session = Depends(get_session)):
    auth_service = AuthService(session)

    try:
        return auth_service.login_user(username, password)
    except Exception:
        raise credentials_exception
