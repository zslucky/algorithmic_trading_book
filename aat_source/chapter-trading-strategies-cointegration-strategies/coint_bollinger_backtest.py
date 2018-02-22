# coint_bollinger_backtest.py

import datetime

import numpy as np

from qstrader import settings
from qstrader.strategy.base import AbstractStrategy
from qstrader.position_sizer.fixed import FixedPositionSizer
from qstrader.event import SignalEvent, EventType
from qstrader.compat import queue
from qstrader.trading_session import TradingSession

from coint_bollinger_strategy import CointegrationBollingerBandsStrategy


def run(config, testing, tickers, filename):
    # Backtest information
    title = [
        'Aluminium Smelting Strategy - ARNC/UNG'
    ]
    initial_equity = 500000.0
    start_date = datetime.datetime(2014, 11, 11)
    end_date = datetime.datetime(2016, 9, 1)

    # Use the Cointegration Bollinger Bands trading strategy
    events_queue = queue.Queue()
    weights = np.array([1.0, -1.213])
    lookback = 15
    entry_z = 1.5
    exit_z = 0.5
    base_quantity = 10000
    strategy = CointegrationBollingerBandsStrategy(
        tickers, events_queue, 
        lookback, weights, 
        entry_z, exit_z, base_quantity
    )

    # Set the position size to use a 
    # fixed base quantity of shares
    position_sizer = FixedPositionSizer(
        default_quantity=base_quantity
    )

    # Set up the backtest
    backtest = TradingSession(
        config, strategy, tickers,
        initial_equity, start_date, end_date,
        events_queue, title=title,
        position_sizer=position_sizer
    )
    results = backtest.start_trading(testing=testing)
    return results


if __name__ == "__main__":
    # Configuration data
    testing = False
    config = settings.from_file(
        settings.DEFAULT_CONFIG_FILENAME, testing
    )
    tickers = ["ARNC", "UNG"]
    filename = None
    run(config, testing, tickers, filename)
