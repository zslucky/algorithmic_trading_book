# intraday_ml_strategy.py

import numpy as np
import pandas as pd
from sklearn.externals import joblib

from qstrader.price_parser import PriceParser
from qstrader.event import (SignalEvent, EventType)
from qstrader.strategy.base import AbstractStrategy


class IntradayMachineLearningPredictionStrategy(AbstractStrategy):
    """
    Requires:
    tickers - The list of ticker symbols
    events_queue - A handle to the system events queue
    """
    def __init__(
        self, tickers, events_queue, 
        model_pickle_file, lags=5
    ):
        self.tickers = tickers
        self.events_queue = events_queue
        self.model_pickle_file = model_pickle_file
        self.lags = lags

        self.invested = False
        self.cur_prices = np.zeros(self.lags+1)
        self.cur_returns = np.zeros(self.lags)
        self.minutes = 0
        self.qty = 10000
        self.model = joblib.load(model_pickle_file)

    def _update_current_returns(self, event):
        """
        Updates the array of current returns "features"
        used by the machine learning model for prediction.
        """
        # Adjust the feature vector to move all lags by one
        # and then recalculate the returns
        for i, f in reversed(list(enumerate(self.cur_prices))):
            if i > 0:
                self.cur_prices[i] = self.cur_prices[i-1]
            else:
                self.cur_prices[i] = event.close_price/float(
                    PriceParser.PRICE_MULTIPLIER
                )
        if self.minutes > (self.lags + 1):
            for i in range(0, self.lags):
                self.cur_returns[i] = ((
                    self.cur_prices[i]/self.cur_prices[i+1]
                )-1.0)*100.0

    def calculate_signals(self, event):
        """
        Calculate the intraday machine learning 
        prediction strategy.
        """
        if event.type == EventType.BAR:
            self._update_current_returns(event)
            self.minutes += 1
            # Allow enough time to pass to populate the 
            # returns feature vector
            if self.minutes > (self.lags + 2):
                pred = self.model.predict(self.cur_returns.reshape((1, -1)))[0]
                # Long only strategy
                if not self.invested and pred == 1:
                    print("LONG: %s" % event.time)
                    self.events_queue.put(
                        SignalEvent(self.tickers[0], "BOT", self.qty)
                    )
                    self.invested = True
                if self.invested and pred == -1:
                    print("CLOSING LONG: %s" % event.time)
                    self.events_queue.put(
                        SignalEvent(self.tickers[0], "SLD", self.qty)
                    )
                    self.invested = False
