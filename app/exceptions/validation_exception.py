from fastapi import status
from app.exceptions.base_exception import BaseAppException


class ValidationException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
