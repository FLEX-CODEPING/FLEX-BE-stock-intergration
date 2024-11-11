class BaseCustomException(Exception):
    def __init__(self, message: str, custom_code: str = "GENERAL_ERROR", details: dict = None):
        self.message = message
        self.custom_code = custom_code
        self.details = details or {}
        super().__init__(self.message)

class KoreaInvestException(BaseCustomException):
    def __init__(self, message: str, custom_code: str = "KIS_ERROR", details: dict = None):
        super().__init__(message, custom_code, details)
