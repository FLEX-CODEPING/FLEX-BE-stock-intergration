from pydantic import BaseModel, Field

class BalanceSheetReq(BaseModel):
    stockCode: str = Field(..., description="필수> 입력 종목코드", max_length=12)
    classCode: str = Field(..., description="필수> 분류 구분 코드 (0: 전체, 1: 분기(연 누적))", max_length=2)