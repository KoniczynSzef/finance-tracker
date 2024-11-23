from auth.utils import is_password_valid
from database.config import get_session
from fastapi import Depends
from models.user import User
from sqlmodel import Session, select


def authenticate_user(username: str, password: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()

    if not user:
        return False

    if not is_password_valid(password, user.hashed_password):
        return False

    return user
