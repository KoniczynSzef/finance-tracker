import os
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from src.auth.schemas import Token
from src.database.config import get_session
from src.models.user import User
from src.schemas.auth_schemas import TokenData
from src.schemas.errors import ValidationError
from src.schemas.user_schemas import UserCreate, UserRead

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class AuthService:
    SECRET_KEY = os.getenv("SECRET_KEY") or "not-so-secret"
    ALGORITHM = os.getenv("HASHING_ALGORITHM") or "not-so-secret"
    ACCESS_TOKEN_EXPIRE_IN_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_IN_MINUTES") or 0)

    oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

    def __init__(self, session: Session = Depends(get_session), password_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")):
        self.session = session
        self.password_context = password_context

    def register_user(self, user: UserCreate):
        existing_user = self.session.exec(select(User).where(
            User.username == user.username)).first()

        if existing_user:
            raise ValueError("User already exists.")

        try:
            new_user = User(**user.model_dump())
        except ValidationError as e:
            raise ValidationError(e.args[0])

        new_user.hashed_password = self.hash_password(user.password)

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)

        return UserRead(**new_user.model_dump())

    def login_user(self, username: str, password: str) -> Token:
        existing_user = self.authenticate_user(username, password)

        if not existing_user:
            raise credentials_exception

        token = self.create_access_token(
            token_data=TokenData(sub=existing_user.username, exp=datetime.now().microsecond))

        return Token(access_token=token, token_type="bearer")

    def authenticate_user(self, username: str, password: str):
        user = self.session.exec(select(User).where(
            User.username == username)).first()

        if not user:
            return False

        if not self.is_password_valid(password, user.hashed_password):
            return False

        return user

    def create_access_token(self, token_data: TokenData, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_IN_MINUTES)):
        to_encode = token_data.model_dump()
        expire = datetime.now() + expires_delta

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def get_current_user(self, token: str = Depends(oauth2_bearer)):
        try:
            payload = jwt.decode(token, self.SECRET_KEY,
                                 algorithms=[self.ALGORITHM])
        except JWTError:
            raise credentials_exception

        user = self.session.exec(select(User).where(
            User.username == payload["sub"])).first()

        if not user:
            raise credentials_exception

        return user

    def is_password_valid(self, plain_password: str, hashed_password: str):
        return self.password_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str):
        return self.password_context.hash(password)
