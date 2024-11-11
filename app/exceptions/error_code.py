from fastapi import status


class ErrorCode:
    KIS_REQUEST_FAIL = {
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "code": "KIS_001",
        "message": "한국투자증권 open API 요청에 실패했습니다."
    }
    KIS_ACCESS_TOKEN_REQUEST_FAIL = {
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "code": "KIS_002",
        "message": "한국투자증권 접근 토큰 발급 요청에 실패했습니다."
    }
    KIS_WEBSOCKET_KEY_REQUEST_FAIL = {
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "code": "KIS_003",
        "message": "한국투자증권 웹소켓 접속 키 발급 요청에 실패했습니다."
    }