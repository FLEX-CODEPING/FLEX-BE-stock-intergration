import yaml
from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect, Body
from fastapi.security import HTTPBearer
import asyncio
from loguru import logger
from app.utils.korea_invest_env import KoreaInvestEnv
from app.services.korea_invest_rest_client import KoreaInvestRestClient
from app.config.swagger_config import setup_swagger
from fastapi.middleware.cors import CORSMiddleware
from app.services.korea_invest_ws_client import KoreaInvestWebSocketClient
from app.dto.request.ranking_fluctuation_request import RankingFluctuationReq
from app.dto.request.daily_trade_volume_request import DailyTradeVolumeReq
from app.dto.request.daily_item_chart_price_request import DailyItemChartPriceReq


app = FastAPI(
    docs_url = "/api/stock-service/swagger-ui.html",
    openapi_url = "/api/stock-service/openapi.json",
    title = "KIS Stock Data Controller"
)

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://do-flex.co.kr:3000",
    "http://dev.do-flex.co.kr:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

setup_swagger(app)
security = HTTPBearer()

with open("./app/config/config.yaml", encoding = 'UTF-8') as f:
    config = yaml.safe_load(f)

env_config = KoreaInvestEnv(config)
base_headers = env_config.get_base_headers()
config = env_config.get_full_config()

stock_router = APIRouter(prefix = "/api/kis/stocks", tags = ["stock"])


@stock_router.get(
    "/{stock_code}/inquire-price",
    summary="주식 현재가 시세 API 요청",
    description="Retrieve the latest price information for a specific stock using its stock code."
)
async def get_inquire_price(stock_code: str):
    config['is_paper_trading'] = True
    korea_invest_client = KoreaInvestRestClient(config, base_headers)
    return korea_invest_client.get_inquire_price(stock_code)


korea_invest_client = KoreaInvestRestClient(config, base_headers)
websocket_url = config['paper_websocket_url'] if config['is_paper_trading'] else config['websocket_url']
korea_invest_websocket = KoreaInvestWebSocketClient(korea_invest_client, websocket_url)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(korea_invest_websocket.run())

@app.websocket("/api/stocks/{stock_code}/real-time")
async def websocket_endpoint(websocket: WebSocket, stock_code: str):
    await websocket.accept()
    try:
        await korea_invest_websocket.subscribe(stock_code) # 주가 정보 subscribe

        while True:
            data = await korea_invest_websocket.get_stock_data(stock_code)
            if data:
                await websocket.send_json(data)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        logger.info(f"Client disconnected for stock {stock_code}")

app.include_router(stock_router)