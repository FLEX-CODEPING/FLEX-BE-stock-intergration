import json
import requests
import copy
from app.core.custom_exception import KoreaInvestException

class KoreaInvestEnv:
    def __init__(self, cfg):
        self.cfg = cfg
        self.cust_type = cfg['cust_type']
        self.base_headers = {
            "Content-Type": "application/json",
            "Accept": "text/plain",
            "charset": "UTF-8",
            "User-Agent": cfg['my_agent'],
        }

        is_paper_trading = cfg['is_paper_trading']
        if is_paper_trading:
            using_url = cfg['paper_url']
            api_key = cfg['paper_api_key']
            api_secret_key = cfg['paper_api_secret_key']
        else:
            using_url = cfg['url']
            api_key = cfg['api_key']
            api_secret_key = cfg['api_secret_key']

        websocket_approval_key = self.get_websocket_approval_key(using_url, api_key, api_secret_key)
        account_access_token = self.get_account_access_token(using_url, api_key, api_secret_key)

        self.base_headers["authorization"] = account_access_token
        self.base_headers["appKey"] = api_key
        self.base_headers["appsecret"] = api_secret_key
        self.cfg['websocket_approval_key'] = websocket_approval_key
        self.cfg['using_url'] = using_url

    def get_base_headers(self):
        return copy.deepcopy(self.base_headers)

    def get_full_config(self):
        return copy.deepcopy(self.cfg)

    def get_account_access_token(self, request_base_url = '', api_key = '', api_secret_key = ''):
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
            raise KoreaInvestException(f"Failed to get account access token: {str(e)}")

    def get_websocket_approval_key(self, request_base_url = '', api_key = '', api_secret_key = ''):
        body = {
            'grant_type': 'client_credentials',
            "appkey": api_key,
            "secretkey": api_secret_key,
        }

        websocket_key_url = f"{request_base_url}/oauth2/Approval"

        try:
            res = requests.post(websocket_key_url, headers = self.base_headers, data = json.dumps(body))
            res.raise_for_status()
            approval_key = res.json().get('approval_key')

            if approval_key is None:
                raise KoreaInvestException("Approval key not found in response.")
            return approval_key
        except requests.exceptions.RequestException as e:
            raise KoreaInvestException(f"Failed to get websocket approval key: {str(e)}")
