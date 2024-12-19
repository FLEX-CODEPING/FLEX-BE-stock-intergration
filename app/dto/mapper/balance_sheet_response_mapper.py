class BalanceSheetResMapper:
    def __init__(self):
        self.mappings = {
            "output": {
                "stac_yymm": "yearMonth",          # 결산연월
                "cras": "curAssets",               # 유동자산
                "fxas": "fixedAssets",             # 비유동자산
                "total_aset": "totalAssets",       # 총자산
                "flow_lblt": "curLiabilities",     # 유동부채
                "fix_lblt": "fixedLiabilities",    # 비유동부채
                "total_lblt": "totalLiabilities",  # 총부채
                "cpfn": "capitalStock",            # 자본금
                "total_cptl": "totalEquity"        # 총자본
            }
        }

    def get_mappings(self):
        return self.mappings