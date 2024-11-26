class RankingMarketCapResMapper:
    def __init__(self):
        self.target_columns = [
            "mksc_shrn_iscd",  # stockCode
            "data_rank",  # ranking
            "hts_kor_isnm",  # corpName
            "stck_prpr",  # curPrice
            "prdy_vrss",  # priceChange
            "prdy_vrss_sign",  # priceChangeSign
            "prdy_ctrt",  # priceChangeRate
            "acml_vol",  # accTradingVol
            "lstn_stcn",  # listedShares
            "stck_avls",
            "mrkt_whol_avls_rlim"
        ]
        
        self.output_columns = [
            "stockCode",
            "ranking",
            "corpName",
            "curPrice",
            "priceChange",
            "priceChangeSign",
            "priceChangeRate",
            "accTradingVol",
            "listedShares",
            "marketCap",
            "marketRatio"
        ]
        
    def get_columns(self):
        return self.target_columns, self.output_columns