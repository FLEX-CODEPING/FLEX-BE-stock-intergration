"""각 엔드포인트에 대한 한국투자증권 open API 를 요청합니다.

module
======
KoreaInvestClient

package
=======
app/services/korea_invest_rest_client.py
"""
from app.utils.korea_invest_api import KoreaInvestApi
from app.dto.request.ranking_fluctuation_request import RankingFluctuationReq
from app.dto.request.daily_trade_volume_request import DailyTradeVolumeReq
from app.dto.request.daily_item_chart_price_request import DailyItemChartPriceReq


class KoreaInvestRestClient(KoreaInvestApi):

    def get_inquire_price(self, stock_no):
        """주식 현재가 시세 API 요청.

            Note: https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-quotations2#L_07802512-4f49-4486-91b4-1050b6f5dc9d
        """
        url = "/uapi/domestic-stock/v1/quotations/inquire-price"
        tr_id = "FHKST01010100"

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD' : stock_no,
        }

        return self._url_fetch(url, tr_id, params)


    def get_daily_trade_volume(self, request: DailyTradeVolumeReq):
        """종목별 일별 매수 & 매도 체결량 API 요청.

            Note: 종목별일별매수매도체결량 [v1_국내주식-056]
            https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-Manalysis#L_4a077f43-7053-47be-b811-8e35be4ea745
        """
        url = "/uapi/domestic-stock/v1/quotations/inquire-daily-trade-volume"
        tr_id = "FHKST03010800"

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': request.stock_code,
            'FID_INPUT_DATE_1': request.date_from.strftime('%Y%m%d'),
            'FID_INPUT_DATE_2': request.date_to.strftime('%Y%m%d'),
            'FID_PERIOD_DIV_CODE': 'D'
        }

        return self._url_fetch(url, tr_id, params)
