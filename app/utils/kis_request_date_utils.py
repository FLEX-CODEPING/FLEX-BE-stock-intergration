from datetime import datetime, timedelta
from app.utils.period_div_code import PeriodDivCode
from app.dto.request.daily_item_chart_price_request import DailyItemChartPriceReq

def get_current_request_date(request: DailyItemChartPriceReq):
    """요청에 따라 새로운 시작 날짜를 계산하는 함수."""
    
    if request.periodDivCode == PeriodDivCode.YEAR.value:
        return get_yearly_new_request_date_from(request.dateTo)
    
    elif request.periodDivCode == PeriodDivCode.MONTH.value:
        return get_monthly_new_request_date_from(request.dateTo)
    
    elif request.periodDivCode == PeriodDivCode.WEEK.value:
        return get_weekly_new_request_date_from(request.dateTo)
    
    elif request.periodDivCode == PeriodDivCode.DAY.value:
        return request.dateTo

def get_yearly_new_request_date_from(date_str):
        """
        주어진 날짜 문자열의 연도를 변경하는 함수.
        """
        date_obj = get_date_obj(date_str)
        
        new_date_obj = date_obj.replace(year=date_obj.year - 1)
        
        return new_date_obj.strftime('%Y%m%d')
    
def get_monthly_new_request_date_from(date_str):
    """
    주어진 날짜 문자열의 전 월에 해당하는 1일 데이터를 반환하는 함수.
    
    """
    date_obj = get_date_obj(date_str)
    
    if date_obj.month == 1:
        first_day_of_previous_month = date_obj.replace(year=date_obj.year - 1, month=12, day=1)
    else:
        first_day_of_previous_month = date_obj.replace(month=date_obj.month - 1, day=1)
    
    return first_day_of_previous_month.strftime('%Y%m%d')

def get_weekly_new_request_date_from(date_str):
    """ 현재 날짜에서 가장 가까운 월요일의 전주 월요일 반환 """
    date_obj = get_date_obj(date_str)
    days_to_subtract = (date_obj.weekday() - 0) % 7
    closest_monday = date_obj - timedelta(days=days_to_subtract)
    
    previous_monday = closest_monday - timedelta(weeks=1)
    
    return previous_monday.strftime('%Y%m%d')

def get_date_obj(date_str):
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    return date_obj
