from scipy.stats import norm
import numpy as np
import pandas as pd 

def Log_returns(df):
    """ Logarithmic retun function.
    Calculates logarithmic returns of adjusted close (Adj Close) of given data frame.
    """
    return np.log(1 + df['Adj Close'].pct_change())

def Drift(df):
    """ Drift function.
    Calculates drift.
    """
    returns_log = Log_returns(df)
    mu = returns_log.mean()
    var = returns_log.var()
    drift = mu - (0.5*var)
    return drift

def MC_daily_returns(df, days, trails):
    """ Monte Carlo simulation function.
    Generates monte carlo simulations for given data frame, simulation days and trails.
    """
    z = norm.ppf(np.random.rand(days, trails))
    returns_std = Log_returns(df).std()
    daily_returns = np.exp(Drift(df) + returns_std*z)
    price_patterns = np.zeros_like(daily_returns)
    price_patterns[0] = df['Adj Close'].iloc[-1]
    for i in range(1, days):
        price_patterns[i] = price_patterns[i - 1]*daily_returns[i]
    expected_val = pd.DataFrame(price_patterns).iloc[-1].mean()
    pct_change = (pd.DataFrame(price_patterns).iloc[-1].mean() - price_patterns[0,0])/pd.DataFrame(price_patterns).iloc[-1].mean()*100
    return pd.DataFrame(price_patterns), expected_val, pct_change