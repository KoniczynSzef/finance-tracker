from fastapi import HTTPException, status


class InvalidCredentials(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class NotFound(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class ValidationError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


UNAUTHORIZED_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User is not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)


def ACTION_ERROR(message: str): return HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=message,
    headers={"WWW-Authenticate": "Bearer"},
)
