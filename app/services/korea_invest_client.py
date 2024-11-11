from loguru import logger
from app.core.custom_exception import KoreaInvestException
from app.utils.korea_invest_api import KoreaInvestAPI


class KoreaInvestClient(KoreaInvestAPI):
    def get_inquire_price(self, stock_no):
        url = "/uapi/domestic-stock/v1/quotations/inquire-price"
        tr_id = "FHKST01010100"

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD' : stock_no,
        }

        try:
            return self._url_fetch(url, tr_id, params)
        except KoreaInvestException as e:
            logger.error(f"Error getting current price: {str(e)}")
            return KoreaInvestException(
                message=f"Request failed: {str(e)}",
                custom_code="KIS_ERROR_REQUEST",
                details={"url": url, "tr_id": tr_id}
            )