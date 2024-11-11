import yaml
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.security import HTTPBearer
from app.utils.korea_invest_env import KoreaInvestEnv
from app.services.korea_invest_client import KoreaInvestClient
from app.config.swagger_config import setup_swagger
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    docs_url = "/api/stock-service/swagger-ui.html",
    openapi_url = "/api/stock-service/openapi.json",
    title = "Stock Controller"
)

setup_swagger(app)
security = HTTPBearer()

with open("./app/config/config.yaml", encoding = 'UTF-8') as f:
    cfg = yaml.safe_load(f)

env_cfg = KoreaInvestEnv(cfg)
base_headers = env_cfg.get_base_headers()
cfg = env_cfg.get_full_config()
korea_invest_client = KoreaInvestClient(cfg, base_headers)

stock_router = APIRouter(prefix = "/api/stocks", tags = ["stock"])


@stock_router.get("/inquire-price/{stock_code}")
async def get_current_price(stock_code: str):
    try:
        price_info_map = korea_invest_client.get_inquire_price(stock_code)

        if not price_info_map:
            raise HTTPException(status_code=404, detail="Stock price information not found")

        return price_info_map
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

app.include_router(stock_router)