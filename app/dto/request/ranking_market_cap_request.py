from pydantic import BaseModel, Field, ConfigDict

class MarketCapRankingReq(BaseModel):
    divClassCode: str = Field(..., description="필수> 분류 구분 코드 (0: 전체, 1:보통주, 2:우선주)", max_length=1)
    stockCode: str = Field(..., description="필수> 입력 종목코드 (0000: 전체, 기타: 업종코드)", max_length=12)
    volCount: str = Field("", description='필수> 거래량 수, 전체 거래량 대상 조회 시 ""(공란) 입력', max_length=12)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "divClassCode": "0",
                "stockCode": "0000",
                "volCount": ""
            }
        }
    )