from fastapi import Depends
from sqlmodel import Session, select

from src.auth.utils import is_password_valid
from src.database.config import get_session
from src.models.user import User


def authenticate_user(username: str, password: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()

    if not user:
        return False

    if not is_password_valid(password, user.hashed_password):
        return False

    return user
