from app.utils.korea_invest_api import KoreaInvestAPI


class KoreaInvestClient(KoreaInvestAPI):
    # 주식 현재가 시세
    def get_inquire_price(self, stock_no):
        url = "/uapi/domestic-stock/v1/quotations/inquire-price"
        tr_id = "FHKST01010100"

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD' : stock_no,
        }

        return self._url_fetch(url, tr_id, params)