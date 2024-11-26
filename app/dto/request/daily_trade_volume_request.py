from pydantic import BaseModel, Field
from datetime import date

class DailyTradeVolumeReq(BaseModel):
    stockCode: str = Field("", description="종목 코드(티커)")
    dateFrom: date = Field(..., description="조회 시작 날짜 (YYYY-MM-DD 형식)")
    dateTo: date = Field(..., description="조회 종료 날짜 (YYYY-MM-DD 형식)")