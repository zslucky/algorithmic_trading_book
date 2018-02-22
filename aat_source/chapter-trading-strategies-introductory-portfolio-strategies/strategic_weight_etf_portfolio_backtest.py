# strategic_weight_etf_portfolio_backtest.py

import datetime

from qstrader import settings
from monthly_rebalance_run import run_monthly_rebalance


if __name__ == "__main__":
    tickers = [
        "SPY", "IJS", "EFA", "EEM", 
        "AGG", "JNK", "DJP", "RWR"
    ]
    ticker_weights = {
        "SPY": 0.25,
        "IJS": 0.05,
        "EFA": 0.20,
        "EEM": 0.05,
        "AGG": 0.20,
        "JNK": 0.05,
        "DJP": 0.10,
        "RWR": 0.10 
    }
    run_monthly_rebalance(
        tickers, ticker_weights, 
        title="Strategic Weight ETF Strategy",
        start_date=datetime.datetime(2007, 12, 4), 
        end_date=datetime.datetime(2016, 10, 12),
        initial_equity=500000.00
    )
