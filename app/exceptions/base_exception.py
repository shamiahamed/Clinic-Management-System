from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "status": "error",
                "message": message
            }
        )
