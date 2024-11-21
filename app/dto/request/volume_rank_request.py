from pydantic import BaseModel, Field

class VolumeRankingReq(BaseModel):
    input_stock_code: str = Field(..., description="필수> 입력 종목코드 (0000: 전체, 기타: 업종코드)", max_length=12)
    class_code: str = Field(..., description="필수> 분류 구분 코드 (0: 전체, 1: 보통주, 2: 우선주)", max_length=2)
    belong_code: str = Field(..., description="필수> 소속 구분 코드", max_length=2)
    target_code: str = Field(..., description="필수> 대상 구분 코드", max_length=32)
    target_exclusion_code: str = Field(..., description="필수> 대상 제외 구분 코드", max_length=32)
    input_price_min: str = Field("", description="필수> 입력 가격, 전체 가격 대상 조회 시 FID_INPUT_PRICE_1, FID_INPUT_PRICE_2 모두 ""(공란) 입력", max_length=12)
    input_price_max: str = Field("", description="필수> 입력 가격2, 전체 가격 대상 조회 시 FID_INPUT_PRICE_1, FID_INPUT_PRICE_2 모두 ""(공란) 입력", max_length=12)
    volume_count: str = Field("", description="필수> 거래량 수, 전체 거래량 대상 조회 시 FID_VOL_CNT ""(공란) 입력", max_length=12)
    input_date_start: str = Field("", description="필수> 입력 날짜1", max_length=10)
