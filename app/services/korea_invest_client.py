"""각 엔드포인트에 대한 한국투자증권 open API 를 요청합니다.

module
======
KoreaInvestClient

package
=======
app/services/korea_invest_client.py
"""
from app.utils.korea_invest_api import KoreaInvestApi


class KoreaInvestClient(KoreaInvestApi):
    """주식 현재가 시세 API 요청.

    Note:
        https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-quotations2#L_07802512-4f49-4486-91b4-1050b6f5dc9d
    """
    def get_inquire_price(self, stock_no):
        url = "/uapi/domestic-stock/v1/quotations/inquire-price"
        tr_id = "FHKST01010100"

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD' : stock_no,
        }

        return self._url_fetch(url, tr_id, params)