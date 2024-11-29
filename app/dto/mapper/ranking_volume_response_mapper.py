class RankingVolumeResMapper:
    def __init__(self):
        self.target_columns = [
            "hts_kor_isnm",  # corpName
            "mksc_shrn_iscd",  # stockCode
            "data_rank",  # ranking
            "stck_prpr",  # curPrice
            "prdy_vrss_sign",  # priceChangeSign
            "prdy_vrss",  # priceChange
            "prdy_ctrt",  # priceChangeRate
            "acml_vol",  # accTradingVolume
            "prdy_vol",  # preDayTradingVolume
            "lstn_stcn",  # listedShares
            "avrg_vol",  # avgTradingVolume
            "n_befr_clpr_vrss_prpr_rate",  # prevPeriodPriceChangeRate
            "vol_inrt",  # volIncreaseRate
            "vol_tnrt",  # volTurnoverRate
            "nday_vol_tnrt",  # periodVolTurnoverRate
            "avrg_tr_pbmn",  # avgTradingValue
            "acml_tr_pbmn"   # accTradingValue
        ]
        
        self.output_columns = [
            "corpName", # 회사명
            "stockCode", # 종목코드
            "ranking", # 순위
            "curPrice", # 현재가
            "priceChangeSign", # 등락부호
            "priceChange", # 등락폭
            "priceChangeRate", # 등락률
            "accTradingVolume", # 누적거래량
            "preDayTradingVolume", # 전일거래량
            "listedShares", # 상장주식수
            "avgTradingVolume", # 평균거래량
            "prevPeriodPriceChangeRate", # 전기간대비등락률
            "volIncreaseRate", # 거래량증가율
            "volTurnoverRate", # 거래회전율
            "periodVolTurnoverRate", # 기간거래회전율
            "avgTradingValue", # 평균거래대금
            "accTradingValue" # 누적거래대금
        ]

    def get_columns(self):
        return self.target_columns, self.output_columns