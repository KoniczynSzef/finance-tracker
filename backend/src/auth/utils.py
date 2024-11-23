from passlib.context import CryptContext

password_context = CryptContext(schemes=["argon2"], deprecated="auto")


def is_password_valid(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str):
    return password_context.hash(plain_password)
