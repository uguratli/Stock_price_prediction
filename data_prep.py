import yfinance as yf
yf.pdr_override()
from pandas_datareader import data as pr
import pandas as pd

import datetime as dt
from dateutil.relativedelta import relativedelta

def Delta_Time(years = 0, months = 0, weeks = 0, days = 0, start = dt.datetime.today()):
    """ Delta time function.
    Creates start and end dates. Years, months, weeks, days are set by default to 0, and start date is set to today.
    """

    start_date = start - relativedelta(years = years, months = months, weeks = weeks, days = days)
    end_date = dt.datetime.today()
    return start_date,end_date

def Stock_data(stocks,start_date,end_date):
    """ Stcok data function.
    Returns stock or market data for given time intervals.
    """
    
    return pr.DataReader(stocks, start=start_date, end=end_date)