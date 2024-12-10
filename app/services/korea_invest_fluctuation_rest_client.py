"""기간별 시세 조회 엔드포인트 대한 한국투자증권 open API 를 요청합니다.

module
======
KoreaInvestClient

package
=======
app/services/korea_invest_fluctuation_rest_client.py
"""

from app.utils.korea_invest_api import KoreaInvestApi
from app.dto.request.daily_item_chart_price_request import DailyItemChartPriceReq
import json
from datetime import datetime, timedelta
from app.exceptions.error_code import ErrorCode
from app.exceptions.custom_exception import BaseCustomException
from app.config.redis_config import redis_client
import json
from app.utils.date_utils import *
import logging
from app.utils.period_div_code import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class KoreaInvestFluctuationRestClient(KoreaInvestApi):
    def __init__(self, config, base_headers):
        super().__init__(config, base_headers)
        self.redis_client = redis_client()

    def _build_new_params(self, request, cur_date_from, cur_date_to):
        """새로운 API 요청 파라미터를 생성하는 함수."""
        return {
            'FID_COND_MRKT_DIV_CODE': request.marketDivCode,
            'FID_INPUT_ISCD': request.stockCode,
            'FID_INPUT_DATE_1': cur_date_from,
            'FID_INPUT_DATE_2': cur_date_to,
            'FID_PERIOD_DIV_CODE': request.periodDivCode,
            'FID_ORG_ADJ_PRC': request.orgAdjPrice,
        }

    def get_daily_item_chart_price(self, request: DailyItemChartPriceReq):
        
        """국내 주식 기간별 시세 (일/주/월/년) API 요청."""
        url = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        tr_id = "FHKST03010100"
        
        today = datetime.now().strftime('%Y%m%d')

        params = self._build_params(request)

        if request.dateTo < today:
            return self._url_fetch(url, tr_id, params)

        new_date_from, new_date_to = get_redis_key_dates(request)
        logging.debug(f"{new_date_from}-{new_date_to}")
        redis_key = f"{request.stockCode}:{request.periodDivCode}:{new_date_from}:{new_date_to}"
        logging.debug(redis_key)
        cached_data = self.redis_client.get(redis_key)

        if cached_data is not None:
            return self._handle_cached_data(request, url, tr_id, cached_data, new_date_to)
        
        return self._transform_kis_response(url, tr_id, params)

    def _build_params(self, request):
        """API 요청에 사용할 기본 파라미터를 생성하는 함수."""
        return {
            'FID_COND_MRKT_DIV_CODE': request.marketDivCode,
            'FID_INPUT_ISCD': request.stockCode,
            'FID_INPUT_DATE_1': request.dateFrom,
            'FID_INPUT_DATE_2': request.dateTo,
            'FID_PERIOD_DIV_CODE': request.periodDivCode,
            'FID_ORG_ADJ_PRC': request.orgAdjPrice,
        }

    def _handle_cached_data(self, request, url, tr_id, cached_data, date_to):
        """캐시된 데이터를 처리하는 함수."""
        cached_data_list = json.loads(cached_data)
        
        cur_request_date_from = get_current_request_date(request)
        
        new_params = self._build_new_params(request, cur_request_date_from, request.dateTo)

        response = self._transform_kis_response(url, tr_id, new_params)
        
        logging.debug(response.output1)

        result = []
        result.append(response.output1) 
        result.append([response.output2[0]] + cached_data_list) 
        return result

