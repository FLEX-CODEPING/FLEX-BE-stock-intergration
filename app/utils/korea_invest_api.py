from collections import namedtuple
from loguru import logger
import json
import requests
from app.core.custom_exception import KoreaInvestException
from app.core.common_response import ApiResponseDTO


class KoreaInvestAPI:
    def __init__(self, cfg, base_headers):
        self.cust_type = cfg['cust_type']
        self._base_headers = base_headers
        self.websocket_approval_key = cfg['websocket_approval_key']
        self.is_paper_trading = cfg['is_paper_trading']
        self.hts_id = cfg['hts_id']
        self.using_url = cfg['using_url']

    def _url_fetch(self, api_url, tr_id, params, is_post_request = False):
        try:
            url = f"{self.using_url}{api_url}"
            headers = self._base_headers

            # 추가 Header 설정
            tr_id = tr_id
            if tr_id[0] in ('T', 'J', 'C'):
                if self.is_paper_trading:
                    tr_id = 'V' + tr_id[1:]

            headers["tr_id"] = tr_id
            headers["cust_type"] = self.cust_type

            if is_post_request:
                res = requests.get(url, headers = headers, data = json.dumps(params))
            else:
                res = requests.get(url, headers = headers, params = params)

            res.raise_for_status()
            api_response = APIResponse(res)
            return api_response.to_api_response_dto()
        except requests.RequestException as e:
            raise KoreaInvestException(
                message = f"Request failed: {str(e)}",
                custom_code = "KIS_REQUEST",
                details = {"url": url, "tr_id": tr_id}
            )


class APIResponse:
    def __init__(self, resp):
        self._res_code = resp.status_code
        self._resp = resp
        self._header = self._set_header()
        self._body = self._set_body()
        self._err_code = self._body.rt_cd
        self._err_message = self._body.msg1

    def get_result_code(self):
        return self._res_code

    def _set_header(self):
        fld = dict()
        for x in self._resp.headers.keys():
            if x.islower():
                fld[x] = self._resp.headers.get(x)
        _th_ = namedtuple('header', fld.keys())
        return _th_(**fld)

    def _set_body(self):
        _tb_ = namedtuple('body', self._resp.json().keys())
        return _tb_(**self._resp.json())

    def get_header(self):
        return self._header

    def get_body(self):
        return self._body

    def get_response(self):
        return self._resp

    def is_ok(self):
        try:
            if self.get_body().rt_cd == '0':
                return True
            else:
                return False
        except:
            return False

    def get_error_code(self):
        return self._err_code

    def get_error_message(self):
        return self._err_message

    def print_all(self):
        logger.info("<Header>")
        for x in self.get_header()._fields:
            logger.info(f'\t-{x}: {getattr(self.get_header(), x)}')
        logger.info("<Body>")
        for x in self.get_body()._fields:
            logger.info(f'\t-{x}: {getattr(self.get_body(), x)}')

    def print_error(self):
        logger.info(f'------------------------------')
        logger.info(f'Error in response: {self.get_result_code()}')
        logger.info(f'{self.get_body().rt_cd}, {self.get_error_code()}, {self.get_error_message()}')
        logger.info(f'------------------------------')

    def to_api_response_dto(self):
        if self.is_ok():
            return ApiResponseDTO(result = self.get_body().output)
        else:
            raise KoreaInvestException(
                message = self.get_error_message(),
                custom_code=f"KIS_ERROR_{self.get_error_code()}",
                details = {"response_body": self.get_body()._asdict()}
            )