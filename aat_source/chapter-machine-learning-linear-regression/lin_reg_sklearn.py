# lin_reg_sklearn.py

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn import linear_model


if __name__ == "__main__":
    # Create N values, with 80% used for training 
    # and 20% used for testing/evaluation
    N = 500
    split = int(0.8*N)

    # Set the intercept and slope of the univariate
    # linear regression simulated data
    alpha = 2.0
    beta = 3.0

    # Set the mean and variance of the randomly
    # distributed noise in the simulated dataset
    eps_mu = 0.0
    eps_sigma = 30.0

    # Set the mean and variance of the X data
    X_mu = 0.0
    X_sigma = 10.0

    # Create the error/noise, X and y data
    eps = np.random.normal(loc=eps_mu, scale=eps_sigma, size=N)
    X = np.random.normal(loc=X_mu, scale=X_sigma, size=N)
    y = alpha + beta*X + eps
    X = X.reshape(-1, 1)  # Needed to avoid deprecation warning

    # Split up the features, X, and responses, y, into
    # training and test arrays
    X_train = X[:split]
    X_test = X[split:]
    y_train = y[:split]
    y_test = y[split:]

    # Open a scikit-learn linear regression model 
    # and fit it to the training data
    lr_model = linear_model.LinearRegression()
    lr_model.fit(X_train, y_train)

    # Output the estimated parameters for the linear model
    print(
        "Estimated intercept, slope: %0.6f, %0.6f" % (
            lr_model.intercept_,
            lr_model.coef_[0]
        )
    )

    # Create a scatterplot of the test data for features
    # against responses, plotting the estimated line
    # of best fit from the ordinary least squares procedure
    plt.scatter(X_test, y_test)
    plt.plot(
        X_test, 
        lr_model.predict(X_test), 
        color='black',
        linewidth=1.0
    )
    plt.xlabel("X")
    plt.ylabel("y")
    plt.show()
