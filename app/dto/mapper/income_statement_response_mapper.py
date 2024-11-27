class IncomeStatementResMapper:
    def __init__(self):
        self.target_columns = [
            "stac_yymm",  # yearMonth
            "sale_account",  # salesRevenue
            "sale_cost",  # costOfSales
            "sale_totl_prfi",  # grossProfit
            "bsop_prti",  # operatingProfit
            "op_prfi",  # ordinaryProfit
            "thtr_ntin"  # netIncomeForThePeriod
        ]
        
        self.output_columns = [
            "yearMonth",
            "salesRevenue",
            "costOfSales",
            "grossProfit",
            "operatingProfit",
            "ordinaryProfit",
            "netIncomeForThePeriod"
        ]

    def get_columns(self):
        return self.target_columns, self.output_columns