"""한국투자증권 open API 를 호출을 담당하며 응답을 표준화하여 반환합니다.

module
======
KoreaInvestApi
KisApiResponse

package
=======
app/utils/korea_invest_api.py
"""
from collections import namedtuple
from loguru import logger
import json
import requests
from app.exceptions.custom_exception import BaseCustomException
from app.core.common_response import CommonResponseDto
from app.exceptions.error_code import ErrorCode
import pandas as pd


class KoreaInvestApi:
    """KoreaInvestApi class 는 한국투자증권 open API 를 호출을 진행합니다.

    Attributes:
        cust_type (str): 고객 유형
        _base_headers (dict): 모든 요청에 사용하는 기본 헤더
        websocket_approval_key (str): WebSocket을 위한 접속 키
        is_paper_trading (bool): 모의 투자 여부
        hts_id (str): 증권 계좌 ID
        using_url (str): API 요청 URL

    Example:
        config = {
            "cust_type": "P",
            "is_paper_trading": True,
            "websocket_approval_key": "ws_key",
            "hts_id": "test_id",
            "using_url": "https://api.com"
        }
        invest_api = KoreaInvestAPI(config, headers)
    """
    def __init__(self, config, base_headers):
        self.cust_type = config['cust_type']
        self._base_headers = base_headers
        self.websocket_approval_key = config['websocket_approval_key']
        self.is_paper_trading = config['is_paper_trading']
        self.hts_id = config['hts_id']
        self.using_url = config['using_url']

    def _fetch_kis_response(self, api_url, tr_id, params, is_post_request=False):
        """KIS API를 호출하고 KisApiResponse 객체를 반환합니다.

        Args:
            api_url (str): API endpoint url
            tr_id (str): 거래 id
            params (dict): API parameters
            is_post_request (bool): POST 요청 여부

        Returns:
            KisApiResponse: KIS API 응답 객체
        """
        try:
            url = f"{self.using_url}{api_url}"
            headers = self._base_headers

            # 추가 Header 설정
            if tr_id[0] in ('T', 'J', 'C'):
                if self.is_paper_trading:
                    tr_id = 'V' + tr_id[1:]
            headers["tr_id"] = tr_id
            headers["custtype"] = self.cust_type

            if is_post_request:
                res = requests.post(url, headers=headers, data=json.dumps(params))
            else:
                res = requests.get(url, headers=headers, params=params)

            res.raise_for_status()
            
            return KisApiResponse(res)  # KIS API 응답 객체 반환

        except requests.RequestException as e:
            raise BaseCustomException(
                ErrorCode.KIS_REQUEST_FAIL,
                details={"url": api_url, "tr_id": tr_id, "exception": str(e)}
            )
    def _transform_kis_response(self, url, tr_id, params, is_post_request=False, mappings=None):
        """KIS API 응답을 컬럼 필터링 및 변환합니다.

        Args:
            url (str): API 요청 URL
            tr_id (str): 거래 ID
            params (dict): API 요청 파라미터
            is_post_request (bool): POST 요청 여부
            mappings (dict): 매핑 규칙

        Returns:
            dict: 필터링 및 변환된 데이터
        """
        kis_response = self._fetch_kis_response(url, tr_id, params, is_post_request)
        
        if kis_response.is_ok():
            body = kis_response.get_body()
            
            if mappings is None:
                return body

            result = {}
            if hasattr(body, "output") and getattr(body, "output"):
                output_data = getattr(body, "output")

                # output_data가 딕셔너리라면 리스트로 변환
                if isinstance(output_data, dict):
                    output_data = [output_data]

                # "output" 매핑
                result = [
                    {mappings["output"].get(k, k): v for k, v in item.items() if k in mappings["output"]}
                    for item in output_data
                ]
                return result  # "output"만 반환

            for key in ["output1", "output2"]:
                if hasattr(body, key) and getattr(body, key):
                    output_data = getattr(body, key)

                    if isinstance(output_data, dict):
                        output_data = [output_data]

                    result[key] = [
                        {mappings[key].get(k, k): v for k, v in item.items() if k in mappings[key]}
                        for item in output_data
                    ]
            return result if result else body


    def _url_fetch(self, url, tr_id, params, is_post_request=False, mappings=None):
        """API 응답을 CommonResponseDto로 반환합니다.

        Args:
            transformed_data (list): 필터링 및 변환된 데이터 리스트

        Returns:
            CommonResponseDto: 처리된 응답 데이터를 포함한 공통 응답 DTO
        """
        transformed_data = self._transform_kis_response(url, tr_id, params, is_post_request, mappings)

        return CommonResponseDto(result=transformed_data)
    
    def get_send_data(self, cmd=None, stockcode=None):
        # 입력값 체크 step
        global tr_type, tr_id
        assert 0 < cmd < 9, f"Wrong Input Data: {cmd}"

        # 입력값에 따라 전송 데이터셋 구분 처리
        if cmd == 1:  # 주식 호가 등록
            tr_id = 'H0STASP0'
            tr_type = '1'
        elif cmd == 2:  # 주식 호가 등록 해제
            tr_id = 'H0STASP0'
            tr_type = '2'
        elif cmd == 3:  # 주식 체결 등록
            tr_id = 'H0STCNT0'
            tr_type = '1'
        elif cmd == 4:  # 주식 체결 등록 해제
            tr_id = 'H0STCNT0'
            tr_type = '2'
        elif cmd == 5:  # 주식 체결 통보 등록 (고객용)
            tr_id = 'H0STCNI0'
            tr_type = '1'
        elif cmd == 6:  # 주식 체결 통보 등록 해제 (고객용)
            tr_id = 'H0STCNI0'
            tr_type = '2'
        elif cmd == 7:  # 주식 체결 통보 등록 (모의)
            tr_id = 'H0STCNI9'
            tr_type = '1'
        elif cmd == 8:  # 주식 체결 통보 등록 해제 (모의)
            tr_id = 'H0STCNI9'
            tr_type = '2'

        # JSON 생성
        senddata = (
            f'{{"header":{{'
            f'"approval_key":"{self.websocket_approval_key}", '
            f'"custtype":"{self.cust_type}", '
            f'"tr_type":"{tr_type}", '
            f'"content-type":"utf-8"}}, '
            f'"body":{{"input":{{'
            f'"tr_id":"{tr_id}", '
            f'"tr_key":"{self.hts_id if cmd in (5, 6, 7, 8) else stockcode}"}}}}}}'
        )

        return senddata


class KisApiResponse:
    """KisApiResponse class 는 API 응답을 처리하고, 응답을 객체로 변환하여 헤더, 본문 등의 정보를 추출 및 관리합니다.

    Attributes:
        _res_code (int): 응답 상태 코드
        _resp (requests.Response): 원본 응답 객체
        _header (namedtuple): 응답 헤더 정보
        _body (namedtuple): 응답 본문 정보
        _err_code (str): 응답 에러 코드
        _err_message (str): 응답 에러 메시지
    """
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
            return self.get_body().rt_cd == '0'
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
        return f"{self.get_error_code()}:{self.get_error_message()}"