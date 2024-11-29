class BalanceSheetResMapper:
    def __init__(self):
        self.target_columns = [
            "stac_yymm",  # yearMonth
            "cras",  # currentAssets
            "fxas",  # fixedAssets
            "total_aset",  # totalAssets
            "flow_lblt",  # currentLiabilities
            "fix_lblt",  # fixedLiabilities
            "total_lblt",  # totalLiabilities
            "cpfn",  # capitalStock
            "total_cptl"  # totalEquity
        ]
        
        self.output_columns = [
        "yearMonth", # 결산연월
        "curAssets", # 유동자산
        "fixedAssets", # 비유동자산
        "totalAssets", # 총자산
        "curLiabilities", # 유동부채
        "fixedLiabilities", # 비유동부채
        "totalLiabilities", # 총부채
        "capitalStock", # 자본금
        "totalEquity" # 총자본
        ]

    def get_columns(self):
        return self.target_columns, self.output_columns