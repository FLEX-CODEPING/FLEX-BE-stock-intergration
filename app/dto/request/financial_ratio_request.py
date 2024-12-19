from pydantic import BaseModel, Field, ConfigDict

class FinalcialRtioReq(BaseModel):
    stockCode: str = Field(...,  description="필수> 입력 종목코드", max_length=12)
    classCode: str = Field(...,  description="필수> 분류 구분 코드 (0: 전체, 1: 분기)", max_length=2)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "stockCode": "005930",
                "classCode": "1"
            }
        }
    )