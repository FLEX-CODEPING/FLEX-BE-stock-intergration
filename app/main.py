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
from app.dto.request.income_statement_request import IncomeStatementReq
from app.dto.request.balance_sheet_request import BalanceSheetReq
from app.config.eureka_client import eureka_lifespan
from app.dto.request.ranking_volume_request import VolumeRankingReq
from app.dto.request.ranking_market_cap_request import MarketCapRankingReq

app = FastAPI(
    lifespan=eureka_lifespan,
    docs_url = "/api/stock-integration-service/swagger-ui.html",
    openapi_url = "/api/stock-integration-service/openapi.json",
    redoc_url="/api/stock-integration-service/redoc",
    title = "Stock Data Integration Controller"
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

with open("./config_kis.yaml", encoding = 'UTF-8') as f:
    config = yaml.safe_load(f)

env_config = KoreaInvestEnv(config)
base_headers = env_config.get_base_headers()
config = env_config.get_full_config()

stock_kis_integration_sheet_router = APIRouter(prefix ="/api/kis/stocks", tags = ["KIS Stock Sheet"])
stock_kis_integration_ranking_router = APIRouter(prefix ="/api/kis/stocks/ranking", tags = ["KIS Stock Ranking"])
stock_kis_integration__fluctuation_router = APIRouter(prefix ="/api/kis/stocks", tags = ["KIS Stock Fluctuation"])


@app.get("/health", include_in_schema=False)
async def health_check():
    logger.info("Handling health check request")
    return {"status": "UP"}


@stock_kis_integration__fluctuation_router.post(
    "/{stock-code}/inquire-price",
    summary="주식 현재가 시세 API 요청"
)
async def get_inquire_price(stock_code: str):
    config['is_paper_trading'] = True
    korea_invest_client = KoreaInvestRestClient(config, base_headers)
    return korea_invest_client.get_inquire_price(stock_code)


@stock_kis_integration__fluctuation_router.post(
    "/daily/trade-volume",
    summary="종목별 일별 매수 & 매도 체결량 API 요청 (종목별일별매수매도체결량 [v1_국내주식-056] - 모의투자 미지원)"
)
async def get_daily_trade_volume(
    request: DailyTradeVolumeReq = Body(...)
):
    config['is_paper_trading'] = False
    korea_invest_client = KoreaInvestRestClient(config, base_headers)
    return korea_invest_client.get_daily_trade_volume(request)

@stock_kis_integration__fluctuation_router.post(
    "/daily/item-chart-price",
    summary="국내 주식 기간별 시세 (일/주/월/년) API 요청 (국내주식기간별시세(일/주/월/년)[v1_국내주식-016])"
)
async def get_daily_item_chart_price(
    request: DailyItemChartPriceReq = Body(...)
):
    config['is_paper_trading'] = True
    korea_invest_client = KoreaInvestRestClient(config, base_headers)
    return korea_invest_client.get_daily_item_chart_price(request)


@stock_kis_integration_ranking_router.post(
    "/fluctuation",
    summary="국내 주식 등락률 순위 API 요청 (국내 주식 등락률 순위[v1_국내주식-088])"
)
async def get_ranking_fluctuation(
    request: RankingFluctuationReq = Body(...)
):
    config['is_paper_trading'] = False
    korea_invest_client = KoreaInvestRestClient(config, base_headers)
    return korea_invest_client.get_ranking_fluctuation(request)


@stock_kis_integration_ranking_router.post(
    "/volume",
    summary="국내주식 거래량순위 API 요청 (거래량순위 [v1_국내주식-047])"
)
async def get_volume_ranking(
    request: VolumeRankingReq = Body(...)
):
    config['is_paper_trading'] = False
    korea_invest_client = KoreaInvestRestClient(config, base_headers)
    return korea_invest_client.get_volume_ranking(request)

@stock_kis_integration_ranking_router.post(
    "/market-cap",
    summary="국내주식 시가총액 상위 API 요청 (국내주식 시가총액 상위[v1_국내주식-091])"
)
async def get_makret_cap_ranking(
    request: MarketCapRankingReq = Body(...)
):
    config['is_paper_trading'] = False
    korea_invest_client = KoreaInvestRestClient(config, base_headers)
    return korea_invest_client.get_makret_cap_ranking(request)


@stock_kis_integration_sheet_router.post(
    "/balance-sheet",
    summary="국내주식 대차대조표 API 요청 (국내주식 대차대조표[v1_국내주식-078])"
)
async def get_volume_ranking(
    request: BalanceSheetReq = Body(...)
):
    config['is_paper_trading'] = False
    korea_invest_client = KoreaInvestRestClient(config, base_headers)
    return korea_invest_client.get_stock_balance_sheet(request)

@stock_kis_integration_sheet_router.post(
    "/income-statement",
    summary="국내주식 손익계산서 API 요청 (국내주식 손익계산서[v1_국내주식-079])"
)
async def get_volume_ranking(
    request: IncomeStatementReq = Body(...)
):
    config['is_paper_trading'] = False
    korea_invest_client = KoreaInvestRestClient(config, base_headers)
    return korea_invest_client.get_stock_income_statement(request)

korea_invest_client = KoreaInvestRestClient(config, base_headers)
websocket_url = config['paper_websocket_url'] if config['is_paper_trading'] else config['websocket_url']
korea_invest_websocket = KoreaInvestWebSocketClient(korea_invest_client, websocket_url)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(korea_invest_websocket.run())

@app.websocket("/ws/kis/stocks/{stock-code}/real-time")
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


app.include_router(stock_kis_integration_sheet_router)
app.include_router(stock_kis_integration_ranking_router)
app.include_router(stock_kis_integration__fluctuation_router)
