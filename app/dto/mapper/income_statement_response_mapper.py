class IncomeStatementResMapper:
    def __init__(self):
        self.mappings = {
            "output": {
                "stac_yymm": "yearMonth",             # 결산 년월
                "sale_account": "salesRevenue",       # 매출액
                "sale_cost": "costOfSales",           # 매출원가
                "sale_totl_prfi": "grossProfit",      # 매출총이익
                "bsop_prti": "operatingProfit",       # 영업이익
                "op_prfi": "ordinaryProfit",          # 경상 이익
                "thtr_ntin": "netIncomeForThePeriod"  # 당기순이익
            }
        }

    def get_mappings(self):
        return self.mappings