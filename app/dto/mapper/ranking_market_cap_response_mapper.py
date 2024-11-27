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
            "stck_avls", # marketCap
            "mrkt_whol_avls_rlim" # marketRatio
        ]
        
        self.output_columns = [
            "stockCode", # 종목코드
            "ranking", # 순위
            "corpName", # 회사명
            "curPrice", # 현재가
            "priceChange", # 등락폭
            "priceChangeSign", # 등락부호
            "priceChangeRate", # 등락률
            "accTradingVol", # 누적거래량
            "listedShares", # 상장주식수
            "marketCap", # 시가총액
            "marketRatio" # 시장비율
        ]
        
    def get_columns(self):
        return self.target_columns, self.output_columns