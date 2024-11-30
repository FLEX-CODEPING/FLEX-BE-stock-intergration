class TradingVolumeResMapper:
    def __init__(self):
        self.mappings = {
            "output1": {
                "shnu_cnqn_smtn": "totalBuyVolume",
                "seln_cnqn_smtn": "totalSellVolume"
            },
            "output2": {
                "stck_bsop_date": "tradingDate",
                "total_seln_qty": "dailySellVolume",
                "total_shnu_qty": "dailyBuyVolume"
            }
        }
    
    def get_mappings(self):
        return self.mappings