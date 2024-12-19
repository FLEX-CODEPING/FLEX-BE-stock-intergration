class FinancialRatioResMapper:
    def __init__(self):
        self.mappings = {
            "output": {
                "stac_yymm": "yearMonth",        # 결산 년월
                "grs": "grs",                    # 매출액 증가율
                "bsop_prfi_inrt": "bsopPrfiInrt",# 영업 이익 증가율
                "ntin_inrt": "ntinInrt",        # 순이익 증가율
                "roe_val": "roeValue",           # ROE 값
                "eps": "eps",                    # 주당순이익
                "sps": "sps",                    # 주당매출액
                "bps": "bps",                    # 주당순자산
                "rsrv_rate": "reserveRate",      # 유보 비율
                "lblt_rate": "liabilityRate"     # 부채 비율
            }
        }

    def get_mappings(self):
        return self.mappings