from pydantic import BaseModel, Field

class VolumeRankingReq(BaseModel):
    stockCode: str = Field(..., description="필수> 입력 종목코드 (0000: 전체, 기타: 업종코드)", max_length=12)
    classCode: str = Field(..., description="필수> 분류 구분 코드 (0: 전체, 1: 보통주, 2: 우선주)", max_length=2)
    belongCode: str = Field(..., description="필수> 소속 구분 코드", max_length=2)
    targetCode: str = Field(..., description="필수> 대상 구분 코드", max_length=32)
    targetExclusionCode: str = Field(..., description="필수> 대상 제외 구분 코드", max_length=32)
    inputPriceMin: str = Field("", description='필수> 입력 가격1, 전체 가격 대상 조회 시 FID_INPUT_PRICE_1, FID_INPUT_PRICE_2 모두 ""(공란) 입력', max_length=12)
    inputPriceMax: str = Field("", description='필수> 입력 가격2, 전체 가격 대상 조회 시 FID_INPUT_PRICE_1, FID_INPUT_PRICE_2 모두 ""(공란) 입력', max_length=12)
    volumeCount: str = Field("", description='필수> 거래량 수, 전체 거래량 대상 조회 시 FID_VOL_CNT ""(공란) 입력', max_length=12)
    inputDateStart: str = Field("", description="필수> 입력 날짜1", max_length=10)