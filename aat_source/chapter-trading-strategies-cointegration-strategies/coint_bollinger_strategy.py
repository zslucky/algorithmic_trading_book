# coint_bollinger_strategy.py

from __future__ import print_function

from collections import deque
from math import floor

import numpy as np

from qstrader.price_parser import PriceParser
from qstrader.event import (SignalEvent, EventType)
from qstrader.strategy.base import AbstractStrategy


class CointegrationBollingerBandsStrategy(AbstractStrategy):
    """
    Requires:
    tickers - The list of ticker symbols
    events_queue - A handle to the system events queue
    lookback - Lookback period for moving avg and moving std
    weights - The weight vector describing 
        a "unit" of the portfolio
    entry_z - The z-score trade entry threshold
    exit_z - The z-score trade exit threshold
    base_quantity - Number of "units" of the portfolio 
        to be traded
    """
    def __init__(
        self, tickers, events_queue, 
        lookback, weights, entry_z, exit_z,
        base_quantity
    ):
        self.tickers = tickers
        self.events_queue = events_queue      
        self.lookback = lookback
        self.weights = weights
        self.entry_z = entry_z
        self.exit_z = exit_z
        self.qty = base_quantity
        self.time = None
        self.latest_prices = np.full(len(self.tickers), -1.0)
        self.port_mkt_val = deque(maxlen=self.lookback)
        self.invested = None
        self.bars_elapsed = 0

    def _set_correct_time_and_price(self, event):
        """
        Sets the correct price and event time for prices
        that arrive out of order in the events queue.
        """
        # Set the first instance of time
        if self.time is None:
            self.time = event.time
        
        # Set the correct latest prices depending upon 
        # order of arrival of market bar event
        price = event.adj_close_price/float(
            PriceParser.PRICE_MULTIPLIER
        )
        if event.time == self.time:
            for i in range(0, len(self.tickers)):
                if event.ticker == self.tickers[i]:
                    self.latest_prices[i] = price
        else:
            self.time = event.time
            self.bars_elapsed += 1
            self.latest_prices = np.full(len(self.tickers), -1.0)
            for i in range(0, len(self.tickers)):
                if event.ticker == self.tickers[i]:
                    self.latest_prices[i] = price

    def go_long_units(self):
        """
        Go long the appropriate number of "units" of the 
        portfolio to open a new position or to close out 
        a short position.
        """
        for i, ticker in enumerate(self.tickers):
            if self.weights[i] < 0.0:
                self.events_queue.put(SignalEvent(
                    ticker, "SLD", 
                    int(floor(-1.0*self.qty*self.weights[i])))
                )
            else:
                self.events_queue.put(SignalEvent(
                    ticker, "BOT", 
                    int(floor(self.qty*self.weights[i])))
                )

    def go_short_units(self):
        """
        Go short the appropriate number of "units" of the 
        portfolio to open a new position or to close out 
        a long position.
        """
        for i, ticker in enumerate(self.tickers):
            if self.weights[i] < 0.0:
                self.events_queue.put(SignalEvent(
                    ticker, "BOT", 
                    int(floor(-1.0*self.qty*self.weights[i])))
                )
            else:
                self.events_queue.put(SignalEvent(
                    ticker, "SLD", 
                    int(floor(self.qty*self.weights[i])))
                )

    def zscore_trade(self, zscore, event):
        """
        Determine whether to trade if the entry or exit zscore
        threshold has been exceeded.
        """
        # If we're not in the market...
        if self.invested is None:
            if zscore < -self.entry_z:  
                # Long Entry
                print("LONG: %s" % event.time)
                self.go_long_units()
                self.invested = "long"
            elif zscore > self.entry_z:  
                # Short Entry
                print("SHORT: %s" % event.time)
                self.go_short_units()
                self.invested = "short"
        # If we are in the market...
        if self.invested is not None:
            if self.invested == "long" and zscore >= -self.exit_z:
                print("CLOSING LONG: %s" % event.time)
                self.go_short_units()
                self.invested = None
            elif self.invested == "short" and zscore <= self.exit_z:
                print("CLOSING SHORT: %s" % event.time)
                self.go_long_units()
                self.invested = None

    def calculate_signals(self, event):
        """
        Calculate the signals for the strategy.
        """
        if event.type == EventType.BAR:
            self._set_correct_time_and_price(event)

            # Only trade if we have all prices
            if all(self.latest_prices > -1.0):
                # Calculate portfolio market value via dot product
                # of ETF prices with portfolio weights
                self.port_mkt_val.append(
                    np.dot(self.latest_prices, self.weights)
                )
                # If there is enough data to form a full lookback
                # window, then calculate zscore and carry out
                # respective trades if thresholds are exceeded
                if self.bars_elapsed > self.lookback:
                    zscore = (
                        self.port_mkt_val[-1] - np.mean(self.port_mkt_val)
                    ) / np.std(self.port_mkt_val)
                    self.zscore_trade(zscore, event)
