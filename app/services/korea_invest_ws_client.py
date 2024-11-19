import json
import websockets
import asyncio
from loguru import logger


class KoreaInvestWebSocketClient:
    def __init__(self, korea_invest_api, websocket_url):
        self.korea_invest_api = korea_invest_api
        self.websocket_url = websocket_url
        self.websocket = None
        self.stock_data = {}
        self.subscribed_stocks = set()  # 이미 구독된 종목 추적

    async def connect(self):
        if not self.websocket or self.websocket.closed:
            self.websocket = await websockets.connect(self.websocket_url, ping_interval=None)
            logger.info("WebSocket connected.")

    async def subscribe(self, stock_code):
        """특정 종목 구독"""
        if stock_code in self.subscribed_stocks:
            logger.info(f"Already subscribed to stock: {stock_code}")
            return  # 이미 구독된 종목이면 요청하지 않음

        if not self.websocket or self.websocket.closed:
            await self.connect()

        # 체결 등록 요청
        send_data = self.korea_invest_api.get_send_data(cmd=3, stockcode=stock_code)
        await self.websocket.send(send_data)
        logger.info(f"[체결 등록 요청] 종목코드: {stock_code}")

        # 호가 등록 요청
        send_data = self.korea_invest_api.get_send_data(cmd=1, stockcode=stock_code)
        await self.websocket.send(send_data)
        logger.info(f"[호가 등록 요청] 종목코드: {stock_code}")

        # 구독 상태 업데이트
        self.subscribed_stocks.add(stock_code)

    async def receive_data(self):
        """실시간 데이터 수신 및 처리"""
        while True:
            try:
                data = await self.websocket.recv()
                logger.info(f"Received data: {data}")

                if data[0] == '0':  # 실시간 데이터
                    recvstr = data.split('|')
                    trid = recvstr[1]

                    if trid == "H0STCNT0":  # 체결 데이터
                        data_dict = self.receive_realtime_tick_domestic(recvstr[3])
                        self.update_stock_data(data_dict['종목코드'], data_dict)
                        logger.info(f"체결 데이터: {data_dict}")

                    elif trid == "H0STASP0":  # 호가 데이터
                        data_dict = self.receive_realtime_hoga_domestic(recvstr[3])
                        self.update_stock_data(data_dict['종목코드'], data_dict)
                        logger.info(f"호가 데이터: {data_dict}")

                else:  # JSON 데이터 처리
                    json_object = json.loads(data)
                    trid = json_object["header"]["tr_id"]

                    if trid == "PINGPONG":
                        await self.websocket.send(data)
                        logger.info(f"### RECV/SEND [PINGPONG] {data}")

            except websockets.exceptions.ConnectionClosed as e:
                logger.error(f"WebSocket connection closed: {e}")
                await self.connect()
            except Exception as e:
                logger.error(f"Error in receive_data: {e}")

    def update_stock_data(self, stock_code, new_data):
        """실시간 데이터 업데이트"""
        if stock_code not in self.stock_data:
            self.stock_data[stock_code] = {}
        self.stock_data[stock_code].update(new_data)

    def receive_realtime_tick_domestic(self, data):
        """체결 데이터 파싱"""
        values = data.split('^')
        return dict(
            종목코드=values[0],
            체결시간=values[1],
            현재가=int(values[2])
        )

    def receive_realtime_hoga_domestic(self, data):
        """호가 데이터 파싱"""
        values = data.split('^')
        data_dict = dict(종목코드=values[0])

        for i in range(1, 11):
            data_dict[f"매수{i}호가"] = values[i + 12]
            data_dict[f"매수{i}호가수량"] = values[i + 32]
            data_dict[f"매도{i}호가"] = values[2 + i]
            data_dict[f"매도{i}호가수량"] = values[22 + i]
        return data_dict

    async def get_stock_data(self, stock_code):
        """특정 종목 데이터 반환"""
        if stock_code not in self.subscribed_stocks:
            await self.subscribe(stock_code)

        await asyncio.sleep(1)  # 데이터 수신 대기
        return self.stock_data.get(stock_code, {})

    async def run(self):
        """WebSocket 연결 시작"""
        await self.connect()
        asyncio.create_task(self.receive_data())