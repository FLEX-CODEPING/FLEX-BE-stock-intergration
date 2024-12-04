from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title = "FLEX KIS 주식 데이터 API",
        version = "1.0",
        routes = app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "in": "header",
            "name": "Authorization",
        }
    }
    openapi_schema["security"] = [{"bearerAuth": []}]

    # WebSocket 명세 추가
    openapi_schema["paths"]["/ws/kis/stocks/real-time"] = {
        "get": {
            "summary": "KIS 실시간 웹소켓 Client",
            "description": (
                "종목 코드에 대해 실시간 체결가 또는 호가 데이터를 수신합니다. "
                "특정 유저가 이미 subscribe 하고 있는 종목 코드를 재요청 할 경우, 호출 상태를 그대로 유지합니다."
            ),
            "parameters": [
                {
                    "name": "stockcode",
                    "in": "parameter",
                    "required": True,
                    "description": "종목 코드 (티커)",
                    "schema": {"type": "string"}
                }
            ],
            "responses": {
                "101": {"description": "WebSocket connection established"},
                "400": {"description": "Invalid stock code"}
            },
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

def setup_swagger(app: FastAPI):
    app.openapi = lambda: custom_openapi(app)
