from pydantic import BaseModel, Field

class RankingFluctuationReq(BaseModel):
    marketCode: str = Field(
        "",
        description=("입력 종목코드. \n"
                     "(0000 - 전체, 코스피: 0001, 코스닥: 1001, 코스피200: 2001)")
    )
    fluctuationRateMin: str = Field("", description="최소 등락 비율. 입력값이 없으면 전체 (비율 ~).")
    fluctuationRateMax: str = Field("", description="최대 등락 비율. 입력값이 없으면 전체 (~ 비율).")
    marketType: str = Field(..., description="조건 시장 분류 코드. 시장 구분 코드 (주식: J).")
    sortOrder: str = Field(
        ...,
        description=(
            "순위 정렬 구분 코드. \n"
            "(0: 상승율순, 1: 하락율순, 2: 시가대비상승율, 3: 시가대비하락율, 4: 변동율.)")
    )
    resultLimit: str = Field(..., description="누적 일수 입력. (0: 전체)")
    priceType: str = Field(
        "",
        description=("가격 구분 코드. \n"
                     "(0 상승율 순일 때: (0: 저가대비, 1: 종가대비). "
                     "1 하락율 순일 때: (0: 고가대비, 1: 종가대비). "
                     "기타: (0: 전체).")
    )
    priceMin: str = Field("", description="최소 가격. 입력값이 없으면 전체 (가격 ~).")
    priceMax: str = Field("", description="최대 가격. 입력값이 없으면 전체 (~ 가격).")
    volumeThreshold: str = Field("", description="거래량 기준. 입력값이 없으면 전체 (거래량 ~).")
    targetType: str = Field("0", description="조회 대상 타입. 0: 전체.")
    excludeType: str = Field("0", description="조회 제외 대상 타입. 0: 전체.")
    categoryType: str = Field("0", description="분류 구분 코드. 0: 전체.")