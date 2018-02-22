# intraday_ml_backtest.py

import datetime

from qstrader import settings
from qstrader.compat import queue
from qstrader.event import SignalEvent, EventType
from qstrader.portfolio_handler import PortfolioHandler
from qstrader.position_sizer.naive import NaivePositionSizer
from qstrader.price_handler.iq_feed_intraday_csv_bar import IQFeedIntradayCsvBarPriceHandler
from qstrader.price_parser import PriceParser
from qstrader.risk_manager.example import ExampleRiskManager
from qstrader.statistics.tearsheet import TearsheetStatistics
from qstrader.strategy.base import AbstractStrategy
from qstrader.trading_session import TradingSession

from intraday_ml_strategy import IntradayMachineLearningPredictionStrategy


def run(config, testing, tickers, filename):
    # Set up variables needed for backtest
    title = [
        "Intraday AREX Machine Learning Prediction Strategy"
    ]
    events_queue = queue.Queue()
    csv_dir = "/path/to/your/csv/data/"
    initial_equity = 500000.0

    # Use DTN IQFeed Intraday Bar Price Handler
    start_date = datetime.datetime(2013, 1, 1)
    end_date = datetime.datetime(2014, 3, 11)
    price_handler = IQFeedIntradayCsvBarPriceHandler(
        csv_dir, events_queue, tickers, start_date=start_date
    )

    # Use the ML Intraday Prediction Strategy
    model_pickle_file = '/path/to/your/ml_model_lda.pkl'
    strategy = IntradayMachineLearningPredictionStrategy(
        tickers, events_queue, model_pickle_file, lags=5
    )

    # Use the Naive Position Sizer where
    # suggested quantities are followed
    position_sizer = NaivePositionSizer()

    # Use an example Risk Manager
    risk_manager = ExampleRiskManager()

    # Use the default Portfolio Handler
    portfolio_handler = PortfolioHandler( 
        PriceParser.parse(initial_equity),
        events_queue, price_handler,
        position_sizer, risk_manager
    )

    # Use the Tearsheet Statistics
    statistics = TearsheetStatistics(
        config, portfolio_handler,
        title=title,
        periods=int(252*6.5*60)  # Minutely periods
    )

    # Set up the backtest
    backtest = TradingSession(
        config, strategy, tickers,
        initial_equity, start_date, end_date,
        events_queue, title=title,
        portfolio_handler=portfolio_handler,
        position_sizer=position_sizer,
        price_handler=price_handler,
        statistics=statistics
    )
    results = backtest.start_trading(testing=testing)
    return results


if __name__ == "__main__":
    # Configuration data
    testing = False
    config = settings.from_file(
        settings.DEFAULT_CONFIG_FILENAME, testing
    )
    tickers = ["AREX"]
    filename = None
    run(config, testing, tickers, filename)
