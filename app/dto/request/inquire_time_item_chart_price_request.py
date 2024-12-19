from pydantic import BaseModel, Field, ConfigDict

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

class InqurieTimeItemChartPriceReq(BaseModel):
    stockCode: str = Field(
        ...,
        description="종목 코드."
    )  # 종목 코드
    time: str = Field(
        "",
        description='조회 시작일자(HHMMSS) ex) "123000" 입력 시 12시 30분 이전부터 1분 간격으로 조회'
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "stockCode": "005930",
                "time": "123000"
            }
        }
    )