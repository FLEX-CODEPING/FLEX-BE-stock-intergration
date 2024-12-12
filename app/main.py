import yaml
from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect, Body, Query
from fastapi.security import HTTPBearer
import asyncio
from loguru import logger
from app.utils.korea_invest_env import KoreaInvestEnv
from app.services.korea_invest_rest_client import KoreaInvestRestClient
from app.services.korea_invest_fluctuation_rest_client import KoreaInvestFluctuationRestClient
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
from app.dto.request.inquire_time_daily_chart_price_request import InqurieTimeDailyChartPriceReq
from app.dto.request.inquire_time_item_chart_price_request import InqurieTimeItemChartPriceReq
from app.core.common_response import CommonResponseDto

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
    "/inquire-price",
    summary="주식 현재가 시세 API 요청"
)
async def get_inquire_price(stockcode: str):
    config['is_paper_trading'] = True
    korea_invest_client = KoreaInvestRestClient(config, base_headers)
    return korea_invest_client.get_inquire_price(stockcode)


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

@stock_kis_integration__fluctuation_router.post(
    "/daily/item-chart-price/cached",
    summary="국내 주식 기간별 시세 (일/주/월/년) API 요청 (국내주식기간별시세(일/주/월/년)[v1_국내주식-016])"
)
async def get_daily_item_chart_price(
    request: DailyItemChartPriceReq = Body(...)
):
    config['is_paper_trading'] = True
    korea_invest_client = KoreaInvestFluctuationRestClient(config, base_headers)

    return CommonResponseDto(result=korea_invest_client.get_daily_item_chart_price(request))

@stock_kis_integration__fluctuation_router.post(
    "/daily/daily-chart-price/inquire-price",
    summary="주식일별분봉조회 API [국내주식-213]"
)
async def get_inqurie_time_daily_chart_price(
    request: InqurieTimeDailyChartPriceReq = Body(...)
):
    config['is_paper_trading'] = True
    korea_invest_client = KoreaInvestRestClient(config, base_headers)
    return korea_invest_client.get_inqurie_time_daily_chart_price(request)

@stock_kis_integration__fluctuation_router.post(
    "/daily/item-chart-price/inquire-price",
    summary="주식당일분봉조회[v1_국내주식-022]"
)
async def get_inqurie_time_item_chart_price(
    request: InqurieTimeItemChartPriceReq = Body(...)
):
    config['is_paper_trading'] = True
    korea_invest_client = KoreaInvestRestClient(config, base_headers)
    return CommonResponseDto(result=korea_invest_client.get_inqurie_time_item_chart_price(request))

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
    summary="국내주식 대차대조표 API 요청 (국내주식 대차대조표[v1_국내주식-078])",
    deprecated= True
)
async def get_volume_ranking(
    request: BalanceSheetReq = Body(...)
):
    """
    **Deprecated**: 이 API는 더 이상 사용되지 않습니다. 
    """
    config['is_paper_trading'] = False
    korea_invest_client = KoreaInvestRestClient(config, base_headers)
    kis_response= korea_invest_client.get_stock_income_statement(request)
    return CommonResponseDto(result=kis_response)

@stock_kis_integration_sheet_router.post(
    "/income-statement",
    summary="국내주식 손익계산서 API 요청 (국내주식 손익계산서[v1_국내주식-079])",
    deprecated= True
)
async def get_volume_ranking(
    request: IncomeStatementReq = Body(...)
):
    """
    **Deprecated**: 이 API는 더 이상 사용되지 않습니다. 
    """
    config['is_paper_trading'] = False
    korea_invest_client = KoreaInvestRestClient(config, base_headers)
    kis_response= korea_invest_client.get_stock_income_statement(request)
    return CommonResponseDto(result=kis_response)

@stock_kis_integration_sheet_router.post(
    "/financial-statements",
    summary="국내주식 손익계산서와 대차대조표 통합 API"
)
async def get_stock_financial_statements(
    stockCode: str = Query(..., description="주식의 고유 코드 (예: 005930)"),
    classCode: str = Query(..., description="분류 구분 코드 (0: 전체, 1: 분기)")):
    """국내주식 손익계산서와 대차대조표 API 요청을 합쳐서 제공."""
    
    income_statement_req = IncomeStatementReq(stockCode=stockCode, classCode=classCode)
    balance_sheet_req = BalanceSheetReq(stockCode=stockCode, classCode=classCode)
    
    config['is_paper_trading'] = False
    korea_invest_client = KoreaInvestRestClient(config, base_headers)

    income_statement = korea_invest_client.get_stock_income_statement(IncomeStatementReq(stockCode=stockCode, classCode=classCode))
    balance_sheet = korea_invest_client.get_stock_balance_sheet(BalanceSheetReq(stockCode=stockCode, classCode=classCode))

    combined_result = {
            "incomeStatementInfo": income_statement,
            "balanceSheetInfo": balance_sheet
    }
    return CommonResponseDto(result=combined_result)


korea_invest_client = KoreaInvestRestClient(config, base_headers)

websocket_url = config['paper_websocket_url'] if config['is_paper_trading'] else config['websocket_url']
korea_invest_websocket = KoreaInvestWebSocketClient(korea_invest_client, websocket_url)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(korea_invest_websocket.run())

@app.websocket("/ws/kis/stocks/real-time")
async def websocket_endpoint(websocket: WebSocket, stockcode: str):
    await websocket.accept()
    try:
        await korea_invest_websocket.subscribe(stockcode) # 주가 정보 subscribe

        while True:
            data = await korea_invest_websocket.get_stock_data(stockcode)
            if data:
                await websocket.send_json(data)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        logger.info(f"Client disconnected for stock {stockcode}")


app.include_router(stock_kis_integration_sheet_router)
app.include_router(stock_kis_integration_ranking_router)
app.include_router(stock_kis_integration__fluctuation_router)
