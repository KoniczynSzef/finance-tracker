from datetime import timedelta
from os import getenv

from auth.actions.authenticate_user import authenticate_user
from auth.actions.create_access_token import create_access_token
from auth.schemas import Token, TokenData
from database.config import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

token_router = APIRouter()

ACCESS_TOKEN_EXPIRE_IN_MINUTES = int(
    getenv("ACCESS_TOKEN_EXPIRE_IN_MINUTES") or 0)


@token_router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_IN_MINUTES)

    access_token = create_access_token(data=TokenData(
        sub=user.username, exp=access_token_expires.seconds), expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
