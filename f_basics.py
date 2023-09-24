import pandas as pd
import numpy as np
from scipy.stats import norm



def VAR(df,confidence_level = 95):
    """ VAR function.
    Returns VAR (Value At Risk) for given stock.
    """
    returns = df["Adj Close"].pct_change().dropna()
    mean = returns.mean()
    std = returns.std()
    return norm.ppf((confidence_level)/100, mean, std)

def Cross_test(df):
    """ Cross test function.
    Checks adjusted close for existance of golden cross and death cross for given data frame.
    """

    df['50_sma'], df['200_sma'] = df['Adj Close'].rolling(50).mean(), df['Adj Close'].rolling(200).mean()
    #df.dropna(inplace= True)
    df['Cross_State'] = df.apply(lambda col: True if col['50_sma'] > col['200_sma'] else False, axis=1)
    Golden_cross_list = []
    Death_cross_list = []
    Death_cross = False
    Golden_cross = False
    for date, state in df['Cross_State'].items():
        if state:
            Death_cross = True
            if Golden_cross:
                Golden_cross_list.append(date)
                Golden_cross =  False
        else:
            Golden_cross = True
            if Death_cross:
                Death_cross_list.append(date)
                Death_cross = False
    return Golden_cross_list, Death_cross_list

def RSI(close, period = 14):
    """ RSI function.
    Returns RSI(Relative Strength Index) for given data frame, period is set by default to 14.
    """
    Delta = close.diff()
    Delta.dropna(inplace = True)
    Gain, Loss = Delta.where(Delta>0,0), -Delta.where(Delta<0,0)
    Gain_m = Gain.rolling(period).mean()
    Loss_m = Loss.rolling(period).mean()
    rsi = 100 - (100/(1 + (Gain_m/Loss_m)))
    return rsi

def Beta(Stock, Market):
    """ Beta function.
    Returns beta and alpha values for given stock and market data frames.
    """
    idx = Stock.index.intersection(Market.index)
    Stock_r, Market_r = Stock['Adj Close'].loc[idx].pct_change().dropna(), Market['Adj Close'].loc[idx].pct_change().dropna()
    try:
        beta, alpha = np.polyfit(Stock_r, Market_r,1)
        return beta, alpha
    except np.linalg.LinAlgError:
        return 0,0

def CAPM(Stock, Market, Risk_free = 0.):
    """ CAPM function.
    Returns CAPM(Capital Asset Pricing Model), risk free rate is set by default to 0.
    """
    idx = Stock.index.intersection(Market.index)
    Market_return = Market['Adj Close'].loc[idx].pct_change().dropna()
    Market_return_annual =Market_return.mean()*252
    beta, alpha = Beta(Stock = Stock, Market = Market)
    ERP = (Market_return_annual - Risk_free) 
    CAPM = Risk_free + beta*ERP
    return CAPM*100

