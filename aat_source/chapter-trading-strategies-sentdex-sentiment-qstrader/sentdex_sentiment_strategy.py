# sentdex_sentiment_strategy.py

from __future__ import print_function

from qstrader.event import (SignalEvent, EventType)
from qstrader.strategy.base import AbstractStrategy


class SentdexSentimentStrategy(AbstractStrategy):
    """
    Requires:
    tickers - The list of ticker symbols
    events_queue - A handle to the system events queue
    sent_buy - Integer entry threshold
    sent_sell - Integer exit threshold
    base_quantity - Number of shares to be traded
    """
    def __init__(
        self, tickers, events_queue, 
        sent_buy, sent_sell, base_quantity
    ):
        self.tickers = tickers
        self.events_queue = events_queue
        self.sent_buy = sent_buy
        self.sent_sell = sent_sell
        self.qty = base_quantity
        self.time = None
        self.invested = dict(
            (ticker, False) for ticker in self.tickers
        )

    def calculate_signals(self, event):
        """
        Calculate the signals for the strategy.
        """
        if event.type == EventType.SENTIMENT:
            ticker = event.ticker
            if ticker != "SPY":
                # Long signal
                if (
                    self.invested[ticker] is False and 
                    event.sentiment >= self.sent_buy
                ):
                    print("LONG %s at %s" % (ticker, event.timestamp))
                    self.events_queue.put(SignalEvent(ticker, "BOT", self.qty))
                    self.invested[ticker] = True
                # Close signal
                if (
                    self.invested[ticker] is True and
                    event.sentiment <= self.sent_sell
                ):
                    print("CLOSING LONG %s at %s" % (ticker, event.timestamp))
                    self.events_queue.put(SignalEvent(ticker, "SLD", self.qty))
                    self.invested[ticker] = False
