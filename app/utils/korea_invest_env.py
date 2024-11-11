"""한국투자증권 open API 호출을 위한 환경 설정을 하고 OAuth 인증을 진행합니다.

module
======
KoreaInvestEnv

package
=======
app/utils/korea_invest_env.py
"""
import json
import requests
import copy
from app.exceptions.custom_exception import BaseCustomException
from app.exceptions.error_code import ErrorCode


class KoreaInvestEnv:
    """KoreaInvestEnv class 는 한국투자증권 open API 호출을 위한 환경변수를 초기화하고 접속 토큰 및 키를 요청합니다.

    Attributes:
        config (dict): config.yaml 정보
        cust_type (str): 고객 타입
        base_headers (dict): 모든 API 요청에 사용할 기본 헤더 설정

    Example:
        config = {
            "cust_type": "P",
            "my_agent": "Mozilla/5.0",
            "is_paper_trading": True,
            "paper_url": "https://paper.api.com",
            "paper_api_key": "dummy_key",
            "paper_api_secret_key": "dummy_secret",
            "url": "https://api.com",
            "api_key": "real_key",
            "api_secret_key": "real_secret"
        }
        invest_env = KoreaInvestEnv(config)
        headers = invest_env.get_base_headers()
    """
    def __init__(self, config):
        self.config = config
        self.cust_type = config['cust_type']
        self.base_headers = {
            "Content-Type": "application/json",
            "Accept": "text/plain",
            "charset": "UTF-8",
            "User-Agent": config['my_agent'],
        }

        # 거래 타입에 따른 URL 과 API key 설정
        is_paper_trading = config['is_paper_trading']
        if is_paper_trading:
            using_url = config['paper_url']
            api_key = config['paper_api_key']
            api_secret_key = config['paper_api_secret_key']
        else:
            using_url = config['url']
            api_key = config['api_key']
            api_secret_key = config['api_secret_key']

        # 접근 토큰 및 키 획득
        websocket_approval_key = self.get_websocket_approval_key(using_url, api_key, api_secret_key)
        account_access_token = self.get_account_access_token(using_url, api_key, api_secret_key)

        # Header update 및 설정 정보 저장
        self.base_headers["authorization"] = account_access_token
        self.base_headers["appKey"] = api_key
        self.base_headers["appsecret"] = api_secret_key
        self.config['websocket_approval_key'] = websocket_approval_key
        self.config['using_url'] = using_url

    def get_base_headers(self):
        """기본 API 헤더 정보를 복사하여 반환합니다.

        Returns:
            dict: API 요청에 사용할 기본 헤더의 복사본
        """
        return copy.deepcopy(self.base_headers)

    def get_full_config(self):
        """전체 환경 설정을 복사하여 반환합니다.

        Returns:
            dict: 구성 정보 복사본
        """
        return copy.deepcopy(self.config)

    def get_account_access_token(self, request_base_url='', api_key='', api_secret_key=''):
        """API 인증용 접근 토큰을 발급받습니다.

        Args:
            request_base_url (str): API 요청 URL
            api_key (str): API key
            api_secret_key (str): API secret key

        Returns:
            str: 계정 접근 토큰 (Bearer 형식)

        Raises:
            BaseCustomException: 토큰 요청 실패 예외
        """
        body = {
            "grant_type": "client_credentials",
            "appkey": api_key,
            "appsecret": api_secret_key,
        }

        access_token_url = f'{request_base_url}/oauth2/tokenP'

        try:
            res = requests.post(access_token_url, data = json.dumps(body), headers = self.base_headers)
            res.raise_for_status()
            my_token = res.json()['access_token']
            return f"Bearer {my_token}"
        except requests.exceptions.RequestException as e:
            raise BaseCustomException(
                ErrorCode.KIS_ACCESS_TOKEN_REQUEST_FAIL,
                details={"Failed to get account access token: ": str(e)}
            )

    def get_websocket_approval_key(self, request_base_url='', api_key='', api_secret_key=''):
        """WebSocket 인증용 접속 키를 발급받습니다.

        Args:
            request_base_url (str): 요청 URL
            api_key (str): API key
            api_secret_key (str): API secret key

        Returns:
            str: WebSocket 접속 키

        Raises:
            BaseCustomException: 접속 키 요청 실패 예외
        """
        body = {
            'grant_type': 'client_credentials',
            "appkey": api_key,
            "secretkey": api_secret_key,
        }

        websocket_key_url = f"{request_base_url}/oauth2/Approval"

        try:
            res = requests.post(websocket_key_url, headers = self.base_headers, data = json.dumps(body))
            res.raise_for_status()
            approval_key = res.json()['approval_key']
            return approval_key
        except requests.exceptions.RequestException as e:
            raise BaseCustomException(
                ErrorCode.KIS_WEBSOCKET_KEY_REQUEST_FAIL,
                details={"Failed to get websocket approval key: ": str(e)}
            )
