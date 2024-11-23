from datetime import datetime, timedelta
from os import getenv

from auth.schemas import TokenData
from jose import jwt

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("HASHING_ALGORITHM")
ACCESS_TOKEN_EXPIRE_IN_MINUTES = int(
    getenv("ACCESS_TOKEN_EXPIRE_IN_MINUTES") or 0)


def create_access_token(data: TokenData, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_IN_MINUTES)):
    if not SECRET_KEY or not ALGORITHM:
        raise ValueError("SECRET_KEY and ALGORITHM must be set!")

    to_encode = data.model_dump()
    expire = datetime.now() + expires_delta

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
