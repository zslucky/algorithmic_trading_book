# pymc3_bayes_stochastic_vol.py

import datetime
import pprint

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import pymc3 as pm
from pymc3.distributions.timeseries import GaussianRandomWalk
import seaborn as sns


def obtain_plot_amazon_prices_dataframe(start_date, end_date):
    """
    Download, calculate and plot the AMZN logarithmic returns.
    """
    print("Downloading and plotting AMZN log returns...")
    amzn = pdr.get_data_yahoo("AMZN", start_date, end_date)
    amzn["returns"] = amzn["Adj Close"]/amzn["Adj Close"].shift(1)
    amzn.dropna(inplace=True)
    amzn["log_returns"] = np.log(amzn["returns"])
    amzn["log_returns"].plot(linewidth=0.5)
    plt.ylabel("AMZN daily percentage returns")
    plt.show()  
    return amzn


def configure_sample_stoch_vol_model(log_returns, samples):
    """
    Configure the stochastic volatility model using PyMC3
    in a 'with' context. Then sample from the model using
    the No-U-Turn-Sampler (NUTS).

    Plot the logarithmic volatility process and then the
    absolute returns overlaid with the estimated vol.
    """
    print("Configuring stochastic volatility with PyMC3...")
    model = pm.Model()
    with model:
        sigma = pm.Exponential('sigma', 50.0, testval=0.1)
        nu = pm.Exponential('nu', 0.1)
        s = GaussianRandomWalk('s', sigma**-2, shape=len(log_returns))
        logrets = pm.StudentT(
            'logrets', nu,
            lam=pm.math.exp(-2.0*s),
            observed=log_returns
        )

    print("Fitting the stochastic volatility model...")
    with model:
        trace = pm.sample(samples)
    pm.traceplot(trace, model.vars[:-1])
    plt.show()

    print("Plotting the log volatility...")
    k = 10
    opacity = 0.03
    plt.plot(trace[s][::k].T, 'b', alpha=opacity)
    plt.xlabel('Time')
    plt.ylabel('Log Volatility')
    plt.show()

    print("Plotting the absolute returns overlaid with vol...")
    plt.plot(np.abs(np.exp(log_returns))-1.0, linewidth=0.5)
    plt.plot(np.exp(trace[s][::k].T), 'r', alpha=opacity)
    plt.xlabel("Trading Days")
    plt.ylabel("Absolute Returns/Volatility")
    plt.show()


if __name__ == "__main__":
    # State the starting and ending dates of the AMZN returns
    start_date = datetime.datetime(2006, 1, 1)
    end_date = datetime.datetime(2015, 12, 31)

    # Obtain and plot the logarithmic returns of Amazon prices
    amzn_df = obtain_plot_amazon_prices_dataframe(start_date, end_date)
    log_returns = np.array(amzn_df["log_returns"])

    # Configure the stochastic volatility model and carry out
    # MCMC sampling using NUTS, plotting the trace
    samples = 2000
    configure_sample_stoch_vol_model(log_returns, samples)
