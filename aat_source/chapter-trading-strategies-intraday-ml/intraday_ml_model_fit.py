# intraday_ml_model_fit.py

import datetime

import numpy as np
import pandas as pd
import sklearn
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import (
    BaggingClassifier, RandomForestClassifier, GradientBoostingClassifier
)
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def create_up_down_dataframe(
    csv_filepath,
    lookback_minutes=30,
    lookforward_minutes=5,
    up_down_factor=2.0,
    percent_factor=0.01,
    start=None, end=None
):
    """
    Creates a Pandas DataFrame that imports and calculates
    the percentage returns of an intraday OLHC ticker from disk.

    'lookback_minutes' of prior returns are stored to create
    a feature vector, while 'lookforward_minutes' are used to
    ascertain how far in the future to predict across.

    The actual prediction is to determine whether a ticker
    moves up by at least 'up_down_factor' x 'percent_factor',
    while not dropping below 'percent_factor' in the same period.

    i.e. Does the stock move up 1% in a minute and not down by 0.5%?

    The DataFrame will consist of 'lookback_minutes' columns for feature
    vectors and one column for whether the stock adheres to the "up/down"
    rule, which is 1 if True or 0 if False for each minute.
    """
    ts = pd.read_csv(
        csv_filepath,
        names=[
            "Timestamp", "Open", "Low", "High",
            "Close", "Volume", "OpenInterest"
        ],
        index_col="Timestamp", parse_dates=True
    )

    # Filter on start/end dates
    if start is not None:
        ts = ts[ts.index >= start]
    if end is not None:
        ts = ts[ts.index <= end]

    # Drop the non-essential columns
    ts.drop(
        [
            "Open", "Low", "High",
            "Volume", "OpenInterest"
        ],
        axis=1, inplace=True
    )

    # Create the lookback and lookforward shifts
    for i in range(0, lookback_minutes):
        ts["Lookback%s" % str(i+1)] = ts["Close"].shift(i+1)
    for i in range(0, lookforward_minutes):
        ts["Lookforward%s" % str(i+1)] = ts["Close"].shift(-(i+1))
    ts.dropna(inplace=True)

    # Adjust all of these values to be percentage returns
    ts["Lookback0"] = ts["Close"].pct_change()*100.0
    for i in range(0, lookback_minutes):
        ts["Lookback%s" % str(i+1)] = ts[
            "Lookback%s" % str(i+1)
        ].pct_change()*100.0
    for i in range(0, lookforward_minutes):
        ts["Lookforward%s" % str(i+1)] = ts[
            "Lookforward%s" % str(i+1)
        ].pct_change()*100.0
    ts.dropna(inplace=True)

    # Determine if the stock has gone up at least by
    # 'up_down_factor' x 'percent_factor' and down no more
    # then 'percent_factor'
    up = up_down_factor*percent_factor
    down = percent_factor

    # Create the list of True/False entries for each date
    # as to whether the up/down logic is true
    down_cols = [
        ts["Lookforward%s" % str(i+1)] > -down
        for i in range(0, lookforward_minutes)
    ]
    up_cols = [
        ts["Lookforward%s" % str(i+1)] > up
        for i in range(0, lookforward_minutes)
    ]
    # Carry out the bitwise and, as well as bitwise or
    # for the down and up logic
    down_tot = down_cols[0]
    for c in down_cols[1:]:
        down_tot = down_tot & c
    up_tot = up_cols[0]
    for c in up_cols[1:]:
        up_tot = up_tot | c
    #ts["UpDown"] = down_tot & up_tot
    ts["UpDown"] = np.sign(ts["Lookforward1"])

    # Convert True/False into 1 and 0
    ts["UpDown"] = ts["UpDown"].astype(int)
    ts["UpDown"].replace(to_replace=0, value=-1, inplace=True)
    return ts


if __name__ == "__main__":
    random_state = 42
    n_estimators = 400
    n_jobs = 1

    csv_filepath = "/path/to/your/AREX.csv"
    lookback_minutes = 30
    lookforward_minutes = 5

    print("Importing and creating CSV DataFrame...")
    start_date = datetime.datetime(2007, 11, 8)
    end_date = datetime.datetime(2012, 12, 31)
    ts = create_up_down_dataframe(
        csv_filepath,
        lookback_minutes=lookback_minutes,
        lookforward_minutes=lookforward_minutes,
        start=start_date, end=end_date
    )

    # Use the first five daily lags of AREX closing prices
    print("Preprocessing data...")
    X = ts[
        [
            "Lookback%s" % str(i)
            for i in range(0, 5)
        ]
    ]
    y = ts["UpDown"]

    # Use the training-testing split with 70% of data in the
    # training data with the remaining 30% of data in the testing
    print("Creating train/test split of data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=random_state
    )
    print("Fitting classifier model...")

    model = LinearDiscriminantAnalysis()

    #model = BaggingClassifier(
    #    base_estimator=DecisionTreeClassifier(),
    #    n_estimators=n_estimators,
    #    random_state=random_state,
    #    n_jobs=n_jobs
    #)

    #model = GradientBoostingClassifier(
    #    n_estimators=n_estimators,
    #    random_state=random_state
    #)

    #model = RandomForestClassifier(
    #    n_estimators=n_estimators,
    #    n_jobs=n_jobs,
    #    random_state=random_state,
    #    max_depth=10
    #)

    model.fit(X_train, y_train)
    #model.fit(X, y)
    print("Outputting metrics...")
    print("Hit-Rate: %s" % model.score(X_test, y_test))
    print("%s\n" % confusion_matrix(model.predict(X_test), y_test))
    print("Pickling model...")
    joblib.dump(model, '/path/to/your/ml_model_lda.pkl')
