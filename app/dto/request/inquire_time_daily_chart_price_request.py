from pydantic import BaseModel, Field, ConfigDict

class InqurieTimeDailyChartPriceReq(BaseModel):
    stockCode: str = Field(
        ...,
        description="종목 코드."
    )  # 종목 코드
    date: str = Field(
        ...,
        description="조회 시작 날짜 (YYYYMMDD 형식). (ex. 20241129)"
    )
    time: str = Field(
        description="입력 시간(HHMMSS) (ex. 153000)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "stockCode": "005930",
                "date": "20241129",
                "time": "153000"
            }
        }
    )
