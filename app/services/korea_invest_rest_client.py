"""각 엔드포인트에 대한 한국투자증권 open API 를 요청합니다.

module
======
KoreaInvestClient

package
=======
app/services/korea_invest_rest_client.py
"""
from app.utils.korea_invest_api import KoreaInvestApi
from app.dto.request.ranking_fluctuation_request import RankingFluctuationReq
from app.dto.request.daily_trade_volume_request import DailyTradeVolumeReq
from app.dto.request.daily_item_chart_price_request import DailyItemChartPriceReq
from app.dto.request.ranking_volume_request import VolumeRankingReq
from app.dto.request.balance_sheet_request import BalanceSheetReq
from app.dto.request.ranking_market_cap_request import MarketCapRankingReq
from app.dto.request.financial_ratio_request import FinalcialRtioReq
from app.dto.mapper.ranking_volume_response_mapper import RankingVolumeResMapper
from app.dto.mapper.income_statement_response_mapper import IncomeStatementResMapper
from app.dto.mapper.balance_sheet_response_mapper import BalanceSheetResMapper
from app.dto.mapper.ranking_market_cap_response_mapper import RankingMarketCapResMapper
from app.dto.mapper.financial_ratio_response_mapper import FinancialRatioResMapper
from app.dto.request.income_statement_request import IncomeStatementReq
from app.dto.mapper.trading_volume_response_mapper import TradingVolumeResMapper
from app.dto.mapper.ranking_fluctuation_response_mapper import RankingFluctuationsMapper


class KoreaInvestRestClient(KoreaInvestApi):

    def get_inquire_price(self, stock_no):
        """주식 현재가 시세 API 요청.

            Note: https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-quotations2#L_07802512-4f49-4486-91b4-1050b6f5dc9d
        """
        url = "/uapi/domestic-stock/v1/quotations/inquire-price"
        tr_id = "FHKST01010100"

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD' : stock_no,
        }

        return self._url_fetch(url, tr_id, params)


    def get_daily_trade_volume(self, request: DailyTradeVolumeReq):
        """종목별 일별 매수 & 매도 체결량 API 요청.

            Note: 종목별일별매수매도체결량 [v1_국내주식-056]
            https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-Manalysis#L_4a077f43-7053-47be-b811-8e35be4ea745
        """
        url = "/uapi/domestic-stock/v1/quotations/inquire-daily-trade-volume"
        tr_id = "FHKST03010800"

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': request.stockCode,
            'FID_INPUT_DATE_1': request.dateFrom.strftime('%Y%m%d'),
            'FID_INPUT_DATE_2': request.dateTo.strftime('%Y%m%d'),
            'FID_PERIOD_DIV_CODE': 'D'
        }
        mappings = TradingVolumeResMapper().get_mappings()
        return self._url_fetch(url, tr_id, params, mappings=mappings)


    def get_ranking_fluctuation(self, request: RankingFluctuationReq):
        """국내 주식 등락률 순위 API 요청.

            Note: 국내 주식 등락률 순위[v1_국내주식-088]
        """
        url = "/uapi/domestic-stock/v1/ranking/fluctuation"
        tr_id = "FHPST01700000"

        params = params = {
            'fid_rsfl_rate2': request.fluctuationRateMax,
            'fid_cond_mrkt_div_code': 'J',
            'fid_cond_scr_div_code': '20170',
            'fid_input_iscd': request.marketCode,
            'fid_rank_sort_cls_code': request.sortOrder,
            'fid_input_cnt_1': request.resultLimit,
            'fid_prc_cls_code': request.priceType,
            'fid_input_price_1': request.priceMin,
            'fid_input_price_2': request.priceMax,
            'fid_vol_cnt': request.volumeThreshold,
            'fid_trgt_cls_code': request.targetType,
            'fid_trgt_exls_cls_code': request.excludeType,
            'fid_div_cls_code': request.categoryType,
            'fid_rsfl_rate1': request.fluctuationRateMin
        }
        mappings = RankingFluctuationsMapper().get_mappings()
        return self._url_fetch(url, tr_id, params, mappings=mappings)


    def get_daily_item_chart_price(self, request: DailyItemChartPriceReq):
        """국내 주식 기간별 시세 (일/주/월/년) API 요청.

            Note: 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
        """
        url = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        tr_id = "FHKST03010100"

        params = {
            'FID_COND_MRKT_DIV_CODE': request.marketDivCode,
            'FID_INPUT_ISCD': request.stockCode,
            'FID_INPUT_DATE_1': request.dateFrom,
            'FID_INPUT_DATE_2': request.dateTo,
            'FID_PERIOD_DIV_CODE': request.periodDivCode,
            'FID_ORG_ADJ_PRC': request.orgAdjPrice,
        }

        return self._url_fetch(url, tr_id, params)
    
    def get_volume_ranking(self, request: VolumeRankingReq):
        """국내주식 거래량순위 API 요청.

            Note: 거래량순위 [v1_국내주식-047]
            최대 30건 확인 가능하며, 다음 조회가 불가함.
        """

        url = "/uapi/domestic-stock/v1/quotations/volume-rank"
        tr_id = "FHPST01710000"

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_COND_SCR_DIV_CODE': '20171',
            'FID_INPUT_ISCD': request.stockCode,
            'FID_DIV_CLS_CODE': request.classCode,
            'FID_BLNG_CLS_CODE': request.belongCode,
            'FID_TRGT_CLS_CODE': "111111111",
            'FID_TRGT_EXLS_CLS_CODE': "000000",
            'FID_INPUT_PRICE_1': request.priceMin,
            'FID_INPUT_PRICE_2': request.priceMax,
            'FID_VOL_CNT': request.volCount,
            'FID_INPUT_DATE_1': ""
            #'FID_INPUT_DATE_1': request.inputDateStart
        }
        mappings = RankingVolumeResMapper().get_mappings()

        return self._url_fetch(url, tr_id, params, mappings=mappings)
    
    def get_stock_income_statement(self, request: IncomeStatementReq):
        """국내주식 손익계산서 API 요청.

            Note: 국내주식 손익계산서[v1_국내주식-079]
        """

        url = "/uapi/domestic-stock/v1/finance/income-statement"
        tr_id = "FHKST66430200"

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': request.stockCode,
            'FID_DIV_CLS_CODE': request.classCode
        }

        mappings = IncomeStatementResMapper().get_mappings()

        return  self._transform_kis_response(url, tr_id, params, mappings=mappings)

    def get_stock_balance_sheet(self, request: BalanceSheetReq):
        """국내주식 대차대조표 API 요청.

            Note: 국내주식 대차대조표[v1_국내주식-078]
        """

        url = "/uapi/domestic-stock/v1/finance/balance-sheet"
        tr_id = "FHKST66430100"

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': request.stockCode,
            'FID_DIV_CLS_CODE': request.classCode
        }

        mappings = BalanceSheetResMapper().get_mappings()

        return self._transform_kis_response(url, tr_id, params, mappings= mappings)

    
    def get_makret_cap_ranking(self, request: MarketCapRankingReq):
        """국내주식 시가총액 상위 API 요청.

            Note: 국내주식 시가총액 상위[v1_국내주식-091]
        """

        url = "/uapi/domestic-stock/v1/ranking/market-cap"
        tr_id = "FHPST01740000"

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            "FID_COND_SCR_DIV_CODE": "20174",
            "FID_DIV_CLS_CODE": request.divClassCode,
            "FID_INPUT_ISCD": request.stockCode,
            "FID_TRGT_CLS_CODE": "0",
            "FID_TRGT_EXLS_CLS_CODE": "0",
            "FID_INPUT_PRICE_1": "",
            "FID_INPUT_PRICE_2": "",
            "FID_VOL_CNT": request.volCount
        }

        mappings = RankingMarketCapResMapper().get_mappings()

        return self._url_fetch(url, tr_id,params=params, mappings=mappings)
    
    def get_stock_info(self, request: FinalcialRtioReq):
        """국내주식 기본정보 API 요청.

            Note: 국내주식 기본정보[v1_국내주식-067]
        """

        url = "/uapi/domestic-stock/v1/quotations/search-stock-info"
        tr_id = "CTPF1002R"

        params = {
            'PRDT_TYPE_CD': '300', #주식
            'PDNO': request.stockCode
        }

        mappings = FinancialRatioResMapper().get_mappings()

        return self._url_fetch(url, tr_id, params, mappings = mappings)