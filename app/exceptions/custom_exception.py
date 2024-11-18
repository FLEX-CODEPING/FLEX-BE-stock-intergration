from fastapi import HTTPException


class BaseCustomException(HTTPException):
    def __init__(self, error_code: dict, details: dict = None):
        self.status_code = error_code["status"]
        self.detail = {
            "code": error_code["code"],
            "message": error_code["message"],
            "details": details or {}
        }

        super().__init__(status_code=self.status_code, detail=self.detail)