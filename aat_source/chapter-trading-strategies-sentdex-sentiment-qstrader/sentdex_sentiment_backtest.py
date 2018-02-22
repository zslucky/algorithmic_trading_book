# sentiment_sentdex_backtest.py

import datetime

from qstrader import settings
from qstrader.compat import queue
from qstrader.event import SignalEvent, EventType
from qstrader.position_sizer.fixed import FixedPositionSizer
from qstrader.sentiment_handler.sentdex_sentiment_handler import SentdexSentimentHandler
from qstrader.strategy.base import AbstractStrategy
from qstrader.trading_session import TradingSession

from sentdex_sentiment_strategy import SentdexSentimentStrategy


def run(config, testing, tickers, filename):
    # Backtest information
    events_queue = queue.Queue()
    title = [
        'Sentiment Sentdex Strategy - Tech Stocks'
        #'Sentiment Sentdex Strategy - Defence Stocks'
        #'Sentiment Sentdex Strategy - Energy Stocks'
    ]
    initial_equity = 500000.0
    start_date = datetime.datetime(2012, 10, 15)
    end_date = datetime.datetime(2016, 2, 2)

    # Use the Sentdex Sentiment trading strategy
    sentiment_handler = SentdexSentimentHandler(
        config.CSV_DATA_DIR, "sentdex_sample.csv",
        events_queue, tickers=tickers, 
        start_date=start_date, end_date=end_date
    )

    # Use the Sentdex Sentiment trading strategy
    base_quantity = 500
    sent_buy = 6
    sent_sell = -1
    strategy = SentdexSentimentStrategy(
        tickers, events_queue, 
        sent_buy, sent_sell, base_quantity
    )

    # Use the Fixed Position Sizer where
    # suggested quantities are followed
    position_sizer = FixedPositionSizer(
        default_quantity=base_quantity
    )

    # Set up the backtest
    backtest = TradingSession(
        config, strategy, tickers,
        initial_equity, start_date, end_date,
        events_queue, title=title,
        position_sizer=position_sizer,
        sentiment_handler=sentiment_handler,
        benchmark="SPY"
    )
    results = backtest.start_trading(testing=testing)
    return results


if __name__ == "__main__":
    # Configuration data
    testing = False
    config = settings.from_file(
        settings.DEFAULT_CONFIG_FILENAME, testing
    )
    tickers = ["MSFT", "AMZN", "GOOG", "AAPL", "IBM", "SPY"]
    #tickers = ["BA", "GD", "LMT", "NOC", "RTN", "SPY"]
    #tickers = ["XOM", "CVX", "SLB", "OXY", "COP", "SPY"]
    filename = None
    run(config, testing, tickers, filename)
