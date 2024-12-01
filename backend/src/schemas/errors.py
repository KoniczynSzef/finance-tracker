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