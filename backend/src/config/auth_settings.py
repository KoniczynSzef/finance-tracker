from os import getenv

from pydantic import BaseModel


class Settings(BaseModel):
    SECRET_KEY: str
    HASHING_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_IN_MINUTES: int


settings = Settings(
    SECRET_KEY=getenv("SECRET_KEY") or "secret",
    HASHING_ALGORITHM=getenv("HASHING_ALGORITHM") or "some-hashing-algorithm",
    ACCESS_TOKEN_EXPIRE_IN_MINUTES=int(
        getenv("ACCESS_TOKEN_EXPIRE_IN_MINUTES") or 0),
)

print(settings)
