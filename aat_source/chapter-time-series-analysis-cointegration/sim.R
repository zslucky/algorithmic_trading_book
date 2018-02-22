library("tseries")

## SIMULATED DATA

## Create a simulated random walk
set.seed(123)
z <- rep(0, 1000)
for (i in 2:1000) z[i] <- z[i-1] + rnorm(1)
plot(z, type="l")

# Plot the autocorrelation of the
# series and its differences
layout(1:2)
acf(z)
acf(diff(z))

# For  x and y series that are
# functions of the z series
x <- y <- rep(0, 1000)
x <- 0.3*z + rnorm(1000)
y <- 0.6*z + rnorm(1000)
layout(1:2)
plot(x, type="l")
plot(y, type="l")

# Form the linear combination "comb"
# and plot its correlogram
comb <- 2*x - y
layout(1:2)
plot(comb, type="l")
acf(comb)

# Carry out the unit root tests
adf.test(comb)
pp.test(comb)
po.test(cbind(2*x,-1.0*y))

# Form a non-stationary linear combination
# and test for unit root with ADF test
badcomb <- -1.0*x + 2.0*y
layout(1:2)
plot(badcomb, type="l")
acf(diff(badcomb))
adf.test(badcomb)
