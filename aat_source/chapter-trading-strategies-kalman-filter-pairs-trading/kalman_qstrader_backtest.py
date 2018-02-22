# kalman_qstrader_backtest.py

import datetime

from qstrader import settings
from qstrader.strategy.base import AbstractStrategy
from qstrader.position_sizer.naive import NaivePositionSizer
from qstrader.event import SignalEvent, EventType
from qstrader.compat import queue
from qstrader.trading_session import TradingSession

from kalman_qstrader_strategy import KalmanPairsTradingStrategy


def run(config, testing, tickers, filename):
    # Backtest information
    title = [
        'Kalman Filter Pairs Trade on TLT/IEI'
    ]
    initial_equity = 100000.0
    start_date = datetime.datetime(2009, 8, 3)
    end_date = datetime.datetime(2016, 8, 1)

    # Use the KalmanPairsTrading Strategy
    events_queue = queue.Queue()
    strategy = KalmanPairsTradingStrategy(
        tickers, events_queue
    )

    # Use the Naive Position Sizer where
    # suggested quantities are followed
    position_sizer = NaivePositionSizer()

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
    tickers = ["TLT", "IEI"]
    filename = None
    run(config, testing, tickers, filename)
