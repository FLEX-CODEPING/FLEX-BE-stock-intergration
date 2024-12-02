class InquireTimeItemChartResMapper:
    def __init__(self):
        self.mappings = {
            "output1": {
                "prdy_vrss": "preDayDifference",  # 전일 대비
                "prdy_vrss_sign": "preDayDifferenceSign",  # 전일 대비 부호
                "prdy_ctrt": "preDayRate",  # 전일 대비율
                "stck_prdy_clpr": "preClosePrice",  # 주식 전일 종가
                "acml_vol": "accVolume",  # 누적 거래량
                "acml_tr_pbmn": "accTradeAmount",  # 누적 거래 대금
                "hts_kor_isnm": "htsKoreanName",  # HTS 한글 종목명
                "stck_prpr": "curPrice"  # 주식 현재가
            },
            "output2": {
                "stck_bsop_date": "tradingDate",  # 주식 영업 일자
                "stck_cntg_hour": "transactionTime",  # 주식 체결 시간
                "acml_tr_pbmn": "accTradeAmount",  # 누적 거래 대금 (중복)
                "stck_prpr": "curPrice",  # 주식 현재가 (중복)
                "stck_oprc": "openPrice",  # 주식 시가2
                "stck_hgpr": "highPrice",  # 주식 최고가
                "stck_lwpr": "lowPrice",  # 주식 최저가
                "cntg_vol": "transactionVolume"  # 체결 거래량
            }
        }

    def get_mappings(self):
        return self.mappings