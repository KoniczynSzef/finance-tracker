class InvalidCredentials(Exception):
    def __init__(self, message: str):
        self.message = message


class NotFound(Exception):
    def __init__(self, message: str):
        self.message = message


class ValidationError(Exception):
    def __init__(self, message: str):
        self.message = message
