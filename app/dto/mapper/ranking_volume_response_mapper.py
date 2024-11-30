class RankingVolumeResMapper:
    def __init__(self):
        self.mappings = {
            "output": {
                "hts_kor_isnm": "corpName",             # 회사명
                "mksc_shrn_iscd": "stockCode",           # 종목코드
                "data_rank": "ranking",                  # 순위
                "stck_prpr": "curPrice",                 # 현재가
                "prdy_vrss_sign": "priceChangeSign",     # 등락부호
                "prdy_vrss": "priceChange",              # 등락폭
                "prdy_ctrt": "priceChangeRate",          # 등락률
                "acml_vol": "accTradingVolume",           # 누적거래량
                "prdy_vol": "preDayTradingVolume",       # 전일거래량
                "lstn_stcn": "listedShares",             # 상장주식수
                "avrg_vol": "avgTradingVolume",          # 평균거래량
                "n_befr_clpr_vrss_prpr_rate": "prevPeriodPriceChangeRate", # 전기간대비등락률
                "vol_inrt": "volIncreaseRate",           # 거래량증가율
                "vol_tnrt": "volTurnoverRate",           # 거래회전율
                "nday_vol_tnrt": "periodVolTurnoverRate",# 기간거래회전율
                "avrg_tr_pbmn": "avgTradingValue",       # 평균거래대금
                "acml_tr_pbmn": "accTradingValue"        # 누적거래대금
            }
        }

    def get_mappings(self):
        return self.mappings