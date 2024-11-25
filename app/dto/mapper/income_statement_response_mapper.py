class IncomeStatementMapper:
    def __init__(self):
        self.target_columns = [
            "stac_yymm",  # settlementYearMonth
            "sale_account",  # salesRevenue
            "sale_cost",  # costOfSales
            "sale_totl_prfi",  # grossProfit
            "bsop_prti",  # operatingProfit
            "op_prfi",  # ordinaryProfit
            "spec_prfi",  # extraordinaryGains
            "spec_loss",  # extraordinaryLosses
            "thtr_ntin"  # netIncomeForThePeriod
        ]
        
        self.output_columns = [
            "yearMonth",
            "salesRevenue",
            "costOfSales",
            "grossProfit",
            "operatingProfit",
            "ordinaryProfit",
            "extraordinaryGains",
            "extraordinaryLosses",
            "netIncomeForThePeriod"
        ]

    def get_columns(self):
        return self.target_columns, self.output_columns