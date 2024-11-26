class RankingMarketCapResMapper:
    def __init__(self):
        self.target_columns = [
            "hts_kor_isnm",  # corpName
            "mksc_shrn_iscd",  # stockCode
            "data_rank",  # ranking
            "stck_prpr",  # curPrice
            "prdy_vrss",  # priceChange
            "prdy_vrss_sign",  # priceChangeSign
            "prdy_ctrt",  # priceChangeRate
            "acml_vol",  # accTradingVol
            "lstn_stcn",  # listedShares
            "avrg_vol",  # avgTradingVolume
        ]
        
        self.output_columns = [
            "corpName",
            "stockCode",
            "ranking",
            "curPrice",
            "priceChange",
            "priceChangeSign",
            "priceChangeRate",
            "accTradingVol",
            "listedShares",
            "marketCap"
        ]