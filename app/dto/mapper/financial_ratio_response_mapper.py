class FinancialRatioResMapper:
    def __init__(self):
        self.target_columns = [
            "stac_yymm",  # yearMonth
            "grs",  # grs
            "bsop_prfi_inrt",  # bsopPrfiInrt
            "ntin_inrt",  # ntin_inrt
            "roe_val",  # roeValue
            "eps",  # eps
            "sps",  # sps
            "bps",  # bps
            "rsrv_rate",  # reserve_rate
            "lblt_rate"  # liability_rate
        ]
        self.output_columns = [
            "yearMonth",  # 결산 년월
            "grs",  # 매출액 증가율
            "bsopPrfiInrt",  # 영업 이익 증가율
            "ntinInrt",  # 순이익 증가율
            "roeValue",  # ROE 값
            "eps",  # 주당순이익
            "sps",  # 주당매출액
            "bps",  # 주당순자산
            "reserveRate",  # 유보 비율
            "liabilityRate"  # 부채 비율
        ]

    def get_columns(self):
        return self.target_columns, self.output_columns