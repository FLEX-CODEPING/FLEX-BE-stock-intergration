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
from app.dto.mapper.ranking_volume_response_mapper import RankingVolumeResMapper
from app.dto.mapper.income_statement_response_mapper import IncomeStatementResMapper
from app.dto.mapper.balance_shhet_response_mapper import BalanceSheetResMapper

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
            'FID_INPUT_ISCD': request.stock_code,
            'FID_INPUT_DATE_1': request.date_from.strftime('%Y%m%d'),
            'FID_INPUT_DATE_2': request.date_to.strftime('%Y%m%d'),
            'FID_PERIOD_DIV_CODE': 'D'
        }

        return self._url_fetch(url, tr_id, params)


    def get_ranking_fluctuation(self, request: RankingFluctuationReq):
        """국내 주식 등락률 순위 API 요청.

            Note: 국내 주식 등락률 순위[v1_국내주식-088]
        """
        url = "/uapi/domestic-stock/v1/ranking/fluctuation"
        tr_id = "FHPST01700000"

        params = params = {
            'fid_rsfl_rate2': request.fluctuation_rate_max,
            'fid_cond_mrkt_div_code': 'J',
            'fid_cond_scr_div_code': '20170',
            'fid_input_iscd': request.market_code,
            'fid_rank_sort_cls_code': request.sort_order,
            'fid_input_cnt_1': request.result_limit,
            'fid_prc_cls_code': request.price_type,
            'fid_input_price_1': request.price_min,
            'fid_input_price_2': request.price_max,
            'fid_vol_cnt': request.volume_threshold,
            'fid_trgt_cls_code': request.target_type,
            'fid_trgt_exls_cls_code': request.exclude_type,
            'fid_div_cls_code': request.category_type,
            'fid_rsfl_rate1': request.fluctuation_rate_min
        }

        return self._url_fetch(url, tr_id, params)


    def get_daily_item_chart_price(self, request: DailyItemChartPriceReq):
        """국내 주식 기간별 시세 (일/주/월/년) API 요청.

            Note: 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
        """
        url = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        tr_id = "FHKST03010100"

        params = {
            'FID_COND_MRKT_DIV_CODE': request.market_div_code,
            'FID_INPUT_ISCD': request.stock_code,
            'FID_INPUT_DATE_1': request.date_from,
            'FID_INPUT_DATE_2': request.date_to,
            'FID_PERIOD_DIV_CODE': request.period_div_code,
            'FID_ORG_ADJ_PRC': request.org_adj_price,
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
            'FID_TRGT_CLS_CODE': request.targetCode,
            'FID_TRGT_EXLS_CLS_CODE': request.targetExclusionCode,
            'FID_INPUT_PRICE_1': request.inputPriceMin,
            'FID_INPUT_PRICE_2': request.inputPriceMax,
            'FID_VOL_CNT': request.volumeCount,
            'FID_INPUT_DATE_1': ""
            #'FID_INPUT_DATE_1': request.inputDateStart
        }
        target_columns, output_columns = RankingVolumeResMapper().get_columns()

        return self._url_fetch(url, tr_id, params, target_columns=target_columns, output_columns=output_columns)
    
    def get_stock_income_statement(self, request: VolumeRankingReq):
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

        target_columns, output_columns = IncomeStatementResMapper().get_columns()

        return self._url_fetch(url, tr_id, params, target_columns=target_columns, output_columns=output_columns)

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

        target_columns, output_columns = BalanceSheetResMapper().get_columns()

        return self._url_fetch(url, tr_id, params, target_columns=target_columns, output_columns=output_columns)