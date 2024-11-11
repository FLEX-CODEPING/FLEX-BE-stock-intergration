from app.exceptions.error_code import ErrorCode
from fastapi import HTTPException
from typing import Optional


class BaseCustomException(HTTPException):
    def __init__(self, error_code: ErrorCode, details: Optional[dict] = None):
        super().__init__(
            status_code = error_code.http_status,
            detail = {
                "custom_code": error_code.custom_code,
                "message": error_code.message,
                "details": details or {}
            }
        )
        self.error_code = error_code
        self.details = details or {}


class KoreaInvestException(BaseCustomException):
    def __init__(self, message: str = None, details: dict = None):
        error_code = ErrorCode.KIS_ERROR
        if message:
            error_code.message = message
        super().__init__(error_code, details)