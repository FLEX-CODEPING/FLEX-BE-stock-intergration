from app.utils.period_div_code import PeriodDivCode
import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_redis_key_dates(periodDivCode: str):
    
    """Redis에 저장된 key의 날짜 형식을 반환"""
    
    # 연봉 (YEAR)
    if periodDivCode == PeriodDivCode.YEAR.value:
        return get_yearly_date_to()  
        
    # 월봉 (MONTH)
    elif periodDivCode == PeriodDivCode.MONTH.value:
        return get_monthly_date_to() 
        
    # 주봉 (WEEK)
    elif periodDivCode == PeriodDivCode.WEEK.value:
        return  get_weekly_date_to().strftime('%Y%m%d')
    
    # 일봉 (DAY)
    elif periodDivCode == PeriodDivCode.DAY.value:
        return get_daily_date_to().strftime('%Y%m%d')


def get_yearly_date_to():
    """
    주어진 날짜 객체의 연도에 해당하는 1월 1일 데이터를 반환하는 함수.
    """
    first_day_of_year = get_date().replace(month=1, day=1)
    return first_day_of_year.strftime('%Y%m%d')

def get_monthly_date_to():
    """
    주어진 날짜 객체의 월에 해당하는 1일 데이터를 반환하는 함수.
    """
    first_day_of_month = get_date().replace(day=1)
    return first_day_of_month.strftime('%Y%m%d')

def get_monthly_date_from(years: int):
    """현재 날짜 기준으로 n년 전 전월 1일을 반환"""
    today = datetime.now()  # 현재 날짜
    four_years_ago = get_date() - relativedelta(years=years)  # 4년 전 날짜
    previous_month = four_years_ago - relativedelta(months=1)  # 4년 전 전월

    first_day_of_previous_month = previous_month.replace(day=1)

    return first_day_of_previous_month.strftime('%Y%m%d')

def get_weekly_date_to():
    """ 현재 날짜에서 가장 가까운 월요일 반환 """
    days_to_subtract = (datetime.now().weekday() - 0) % 7
    closest_monday = datetime.now() - timedelta(days=days_to_subtract)
    
    return closest_monday

def get_weekly_date_from(periods: int):
    """ 현재 날짜에서 가장 가까운 월요일 기준으로 n 주전의 날짜 반환 """
    date = get_weekly_date_to()
    weeks_ago = timedelta(weeks=periods)
    date_80_weeks_ago = date - weeks_ago

    return date_80_weeks_ago.strftime('%Y%m%d')

def get_daily_date_to():
    """오늘 기준으로 전일(어제)을 반환하는 함수"""
    today = datetime.now() 
    previous_day = today - timedelta(days=1)  
    return previous_day

def get_daily_date_from(periods: int):
    """전일 기준으로 n개월 전의 날짜를 반환하는 함수"""
    previous_day = get_daily_date_to()
    four_months_ago = previous_day - relativedelta(months=periods) 
    return four_months_ago.strftime('%Y%m%d') 

def get_date():
    return datetime.now()