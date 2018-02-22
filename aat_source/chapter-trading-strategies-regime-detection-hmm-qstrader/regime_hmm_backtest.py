# regime_hmm_backtest.py

import datetime
import pickle

import numpy as np

from qstrader import settings
from qstrader.compat import queue
from qstrader.event import SignalEvent, EventType
from qstrader.portfolio_handler import PortfolioHandler
from qstrader.position_sizer.naive import NaivePositionSizer
from qstrader.price_handler.yahoo_daily_csv_bar import \
    YahooDailyCsvBarPriceHandler
from qstrader.price_parser import PriceParser
from qstrader.risk_manager.example import ExampleRiskManager
from qstrader.statistics.tearsheet import TearsheetStatistics
from qstrader.strategy.base import AbstractStrategy
from qstrader.trading_session import TradingSession

from regime_hmm_strategy import MovingAverageCrossStrategy
from regime_hmm_risk_manager import RegimeHMMRiskManager


def run(config, testing, tickers, filename):
    # Backtest information
    title = [
        #'Trend Following Regime Detection without HMM'
        'Trend Following Regime Detection with HMM'
    ]
    pickle_path = "/path/to/your/model/hmm_model_spy.pkl"
    events_queue = queue.Queue()
    csv_dir = config.CSV_DATA_DIR
    initial_equity = 500000.00
    start_date = datetime.datetime(2005, 1, 1)
    end_date = datetime.datetime(2014, 12, 31)

    # Use the Moving Average Crossover trading strategy
    base_quantity = 10000
    strategy = MovingAverageCrossStrategy(
        tickers, events_queue, base_quantity,
        short_window=10, long_window=30
    )

    # Use Yahoo Daily Price Handler
    price_handler = YahooDailyCsvBarPriceHandler(
        csv_dir, events_queue, tickers,
        start_date=start_date, 
        end_date=end_date,
        calc_adj_returns=True
    )

    # Use the Naive Position Sizer 
    # where suggested quantities are followed
    position_sizer = NaivePositionSizer()

    # Use an example Risk Manager
    #risk_manager = ExampleRiskManager()
    # Use regime detection HMM risk manager
    hmm_model = pickle.load(open(pickle_path, "rb"))
    risk_manager = RegimeHMMRiskManager(hmm_model)
    
    # Use the default Portfolio Handler
    portfolio_handler = PortfolioHandler(
        PriceParser.parse(initial_equity), 
        events_queue, price_handler,
        position_sizer, risk_manager
    )

    # Use the Tearsheet Statistics class
    statistics = TearsheetStatistics(
        config, portfolio_handler, 
        title, benchmark="SPY"
    )

    # Set up the backtest
    backtest = TradingSession(
        config, strategy, tickers,
        initial_equity, start_date, end_date,
        events_queue, title=title,
        price_handler=price_handler,
        position_sizer=position_sizer,
        risk_manager=risk_manager,
        statistics=statistics,
        portfolio_handler=portfolio_handler
    )
    results = backtest.start_trading(testing=testing)
    return results


if __name__ == "__main__":
    # Configuration data
    testing = False
    config = settings.from_file(
        settings.DEFAULT_CONFIG_FILENAME, testing
    )
    tickers = ["SPY"]
    filename = None
    run(config, testing, tickers, filename)
