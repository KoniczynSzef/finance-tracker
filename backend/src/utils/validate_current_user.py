from src.models.user import User
from src.schemas.errors import UNAUTHORIZED_ERROR


def validate_current_user(user: User):
    if not user or not user.id:
        raise UNAUTHORIZED_ERROR

    return user.id
