from fastapi import status


class CustomException(Exception):
    code = status.HTTP_502_BAD_GATEWAY
    message = "Bad Gateway"

    def __init__(
        self, message: str | None = None, errors: dict[str, str] | None = None
    ):
        self.message = message or self.message
        self.errors = errors

    def __str__(self) -> str:
        if self.errors and isinstance(self.errors, dict):
            return f"{self.message} -> {self.errors.get('en', '')}"
        return self.message


class ValidationException(CustomException):
    code = status.HTTP_400_BAD_REQUEST
    message = "Validation failed"


class DatabaseError(CustomException):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Database Error"