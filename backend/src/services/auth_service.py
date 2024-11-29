from database.config import get_session
from fastapi import Depends
from passlib.context import CryptContext
from sqlmodel import Session


class AuthService:
    def __init__(self, session: Session = Depends(get_session), password_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")):
        self.session = session
        self.password_context = password_context

    def authenticate_user(self, username: str, password: str):
        pass

    def create_access_token(self, user_id: int):
        pass

    def get_current_user(self, token: str):
        pass

    def is_password_valid(self, password: str):
        pass
