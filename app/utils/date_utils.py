from datetime import datetime 
from app.utils.period_div_code import PeriodDivCode
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_redis_key_dates(request):
        """Redis에 저장된 날짜 형식을 반환"""
        if request.periodDivCode == PeriodDivCode.YEAR.value:
            new_date_from = get_first_day_of_month(request.dateFrom)
            new_date_to = get_first_day_of_year(request.dateTo) 
        elif request.periodDivCode == PeriodDivCode.MONTH.value:
            new_date_from = get_first_day_of_month(request.dateFrom) # 4년전 전월 1일
            new_date_to = get_first_day_of_month(request.dateTo) # 당월의 1일
        else:
            new_date_to = ''
            new_date_from = ''
        return new_date_from, new_date_to
        
def get_current_request_date(request):
    """요청에 따라 새로운 시작 및 종료 날짜를 계산하는 함수."""
    if request.periodDivCode == PeriodDivCode.YEAR.value:
        return change_to_last_year(request.dateFrom)
    elif request.periodDivCode == PeriodDivCode.MONTH.value:
        return get_first_day_of_previous_month(request.dateFrom)
        
def change_to_last_year(date_str):
        """
        주어진 날짜 문자열의 연도를 변경하는 함수.
        """
        date_obj = datetime.strptime(date_str, '%Y%m%d')
        
        new_date_obj = date_obj.replace(year=date_obj.year - 1)
        
        return new_date_obj.strftime('%Y%m%d')
    
def get_first_day_of_year(date_str):
        """
        주어진 날짜 문자열의 연도에 해당하는 1월 1일 데이터를 반환하는 함수.
        """
        date_obj = datetime.strptime(date_str, '%Y%m%d')
        
        first_day_of_year = date_obj.replace(month=1, day=1)
        
        return first_day_of_year.strftime('%Y%m%d')

def get_first_day_of_month(date_str):
    """
    주어진 날짜 문자열의 월에 해당하는 1일 데이터를 반환하는 함수.
    
    """
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    
    first_day_of_month = date_obj.replace(day=1)
    
    return first_day_of_month.strftime('%Y%m%d')

def get_first_day_of_previous_month(date_str):
    """
    주어진 날짜 문자열의 전 월에 해당하는 1일 데이터를 반환하는 함수.
    
    """
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    
    if date_obj.month == 1:
        first_day_of_previous_month = date_obj.replace(year=date_obj.year - 1, month=12, day=1)
    else:
        first_day_of_previous_month = date_obj.replace(month=date_obj.month - 1, day=1)
    
    return first_day_of_previous_month.strftime('%Y%m%d')