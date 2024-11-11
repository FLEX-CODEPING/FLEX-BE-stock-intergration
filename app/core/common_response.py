from pydantic import BaseModel
from typing import Optional, Any


class ApiResponseDTO(BaseModel):
    isSuccess: bool = True
    code: str = "COMMON_200"
    message: str = "성공"
    result: Optional[Any] = None
