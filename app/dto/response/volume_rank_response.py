from pydantic import BaseModel, Field

class RankingVolumeRes(BaseModel):
    corpName: str = Field(..., description="종목명")
    stockcode: str = Field(..., description="종목 코드")
    ranking: int = Field(..., description="순위")
    curPrice: int = Field(..., description="현재가")
    priceChangeSign: str = Field(..., description="가격 변동 부호 (+/-/0)")
    priceChange: int = Field(..., description="가격 변동 금액")
    priceChangeRate: float = Field(..., description="가격 변동 비율")
    accTradingVolume: int = Field(..., description="누적 거래량")
    preDayTradingVolume: int = Field(..., description="전일 거래량")
    listedShares: int = Field(..., description="상장 주식 수")
    avgTradingVolume: int = Field(..., description="평균 거래량")
    prevPeriodPriceChangeRate: float = Field(..., description="이전 기간 대비 가격 변동률")
    volIncreaseRate: float = Field(..., description="거래량 증가율")
    volTurnoverRate: float = Field(..., description="거래량 회전율")
    periodVolTurnoverRate: float = Field(..., description="특정 기간 거래량 회전율")
    avgTradingValue: int = Field(..., description="평균 거래 대금")
    # valueTurnoverRate: float = Field(..., description="거래 대금 회전율")
    # periodValueTurnoverRate: float = Field(..., description="특정 기간 거래 대금 회전율")
    accTradingValue: int = Field(..., description="누적 거래 대금")

    output_columns = [
                        "corpName",
                        "stockCode",
                        "ranking",
                        "curPrice",
                        "priceChangeSign",
                        "priceChange",
                        "priceChangeRate",
                        "accTradingVolume",
                        "preDayTradingVolume",
                        "listedShares",
                        "avgTradingVolume",
                        "prevPeriodPriceChangeRate",
                        "volIncreaseRate",
                        "volTurnoverRate",
                        "periodVolTurnoverRate",
                        "avgTradingValue",
                        "accTradingValue"
                    ]
