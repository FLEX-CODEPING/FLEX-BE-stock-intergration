class RankingMarketCapResMapper:
    def __init__(self):
        self.mappings = {
            "output": {
                "mksc_shrn_iscd": "stockCode",        # 종목코드
                "data_rank": "ranking",                # 순위
                "hts_kor_isnm": "corpName",           # 회사명
                "stck_prpr": "curPrice",               # 현재가
                "prdy_vrss": "priceChange",            # 등락폭
                "prdy_vrss_sign": "priceChangeSign",   # 등락부호
                "prdy_ctrt": "priceChangeRate",        # 등락률
                "acml_vol": "accTradingVol",           # 누적거래량
                "lstn_stcn": "listedShares",           # 상장주식수
                "stck_avls": "marketCap",              # 시가총액
                "mrkt_whol_avls_rlim": "marketRatio"   # 시장비율
            }
        }
        
    def get_mappings(self):
        return self.mappings