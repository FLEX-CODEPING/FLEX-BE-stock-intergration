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
            "yearMonth",
            "curAssets",
            "fixedAssets",
            "totalAssets",
            "curLiabilities",
            "fixedLiabilities",
            "totalLiabilities",
            "capitalStock",
            "totalEquity"
        ]

    def get_columns(self):
        return self.target_columns, self.output_columns