from enum import Enum
from starlette.status import *

class ErrorCode(Enum):
    KIS_REQUEST_ERROR = (HTTP_500_INTERNAL_SERVER_ERROR, "KIS_REQUEST_ERROR", "KoreaInvestAPI Error")

    def __init__(self, http_status, custom_code, message):
        self.http_status = http_status
        self.custom_code = custom_code
        self.message = message