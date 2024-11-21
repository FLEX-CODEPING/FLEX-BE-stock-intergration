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

    def get_columns(self):
        return self.target_columns, self.output_columns