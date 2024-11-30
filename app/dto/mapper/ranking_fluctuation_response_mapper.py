class RankingFluctuationsMapper:
    def __init__(self):        
        self.mappings = {
            "output": {
                "stck_shrn_iscd": "stockCode",                  # 주식 단축 종목코드
                "data_rank": "dataRank",                       # 데이터 순위
                "hts_kor_isnm": "stockName",                   # HTS 한글 종목명
                "stck_prpr": "curPrice",                   # 주식 현재가
                "prdy_vrss": "priceChange",                   # 전일 대비
                "prdy_vrss_sign": "priceChangeSign",          # 전일 대비 부호
                "prdy_ctrt": "priceChangeRate",               # 전일 대비율
                "acml_vol": "accVolume",              # 누적 거래량
                "stck_hgpr": "highPrice",                     # 주식 최고가
                "hgpr_hour": "highPriceTime",                 # 최고가 시간
                "acml_hgpr_date": "highPriceDate",            # 누적 최고가 일자
                "stck_lwpr": "lowPrice",                      # 주식 최저가
                "lwpr_hour": "lowPriceTime",                  # 최저가 시간
                "acml_lwpr_date": "lowPriceDate",             # 누적 최저가 일자
                "lwpr_vrss_prpr_rate": "lowPriceToCurRate", # 최저가 대비 현재가 비율
                "dsgt_date_clpr_vrss_prpr_rate": "closingPriceToCurRate", # 지정 일자 종가 대비 현재가 비율
                "cnnt_ascn_dynu": "continuousRiseDays",       # 연속 상승 일수
                "hgpr_vrss_prpr_rate": "highPriceToCurRate", # 최고가 대비 현재가 비율
                "cnnt_down_dynu": "continuousFallDays",       # 연속 하락 일수
                "oprc_vrss_prpr_sign": "openPriceChangeSign", # 시가2 대비 현재가 부호
                "oprc_vrss_prpr": "openPriceChange",       # 시가2 대비 현재가
                "oprc_vrss_prpr_rate": "openPriceChangeRate", # 시가2 대비 현재가 비율
                "prd_rsfl": "periodChange",                   # 기간 등락
                "prd_rsfl_rate": "periodChangeRate"           # 기간 등락 비율
            }
        }

    def get_mappings(self):
        return self.mappings