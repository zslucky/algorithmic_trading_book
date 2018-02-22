# exponential_plot.py

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == "__main__":
    sns.set_palette("deep", desat=.6)
    sns.set_context(rc={"figure.figsize": (8, 4)})
    x = np.linspace(0.0, 5.0, 100)
    lambdas = [0.5, 1.0, 2.0]
    for lam in lambdas:
        y = lam*np.exp(-lam*x)
        ax = plt.plot(x, y, label="$\\lambda=%s$" % lam)
    plt.xlabel("x")
    plt.ylabel("P(x)")
    plt.legend(title="Parameters")
    plt.show()
