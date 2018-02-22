# Create an AR(1) proces, plotting its values
# and correlogram, for alpha_1 = 0.6
set.seed(1)
x <- w <- rnorm(100)
for (t in 2:100) x[t] <- 0.6*x[t-1] + w[t]
layout(1:2)
plot(x, type="l")
acf(x)

# Fit an autoregressive model to the series
# previously generated, outputting its order,
# parameter estimates and confidence intervals
x.ar <- ar(x, method = "mle")
x.ar$order
x.ar$ar
x.ar$ar + c(-1.96, 1.96)*sqrt(x.ar$asy.var)

# Create an AR(1) proces, plotting its values
# and correlogram, for alpha_1 = -0.6
set.seed(1)
x <- w <- rnorm(100)
for (t in 2:100) x[t] <- -0.6*x[t-1] + w[t]
layout(1:2)
plot(x, type="l")
acf(x)

# Fit an autoregressive model to the series
# previously generated, outputting its order,
# parameter estimates and confidence intervals
x.ar <- ar(x, method = "mle")
x.ar$order
x.ar$ar
x.ar$ar + c(-1.96, 1.96)*sqrt(x.ar$asy.var)

# Create an AR(2) proces, plotting its values
# and correlogram, for alpha_1 = 0.666 and
# alpha_2 = -0.333
set.seed(1)
x <- w <- rnorm(100)
for (t in 3:100) x[t] <- 0.666*x[t-1] - 0.333*x[t-2] + w[t]
layout(1:2)
plot(x, type="l")
acf(x)

# Fit an autoregressive model to the series
# previously generated, outputting its order and
# parameter estimates
x.ar <- ar(x, method = "mle")
x.ar$order
x.ar$ar

# Plot daily closing prices for Amazon Inc. (AMZN)
require(quantmod)
getSymbols("AMZN")
plot(Cl(AMZN))

# Create differenced log returns of AMZN
# and plot their values and correlogram
amznrt = diff(log(Cl(AMZN)))
plot(amznrt)
acf(amznrt, na.action=na.omit)

# Fit an autoregressive model to AMZN log returns
# outputting its order and parameter estimates
# and confidence intervals
amznrt.ar <- ar(amznrt, na.action=na.omit)
amznrt.ar$order
amznrt.ar$ar
amznrt.ar$asy.var
-0.0278 + c(-1.96, 1.96)*sqrt(4.59e-4)
-0.0687 + c(-1.96, 1.96)*sqrt(4.59e-4)

# Plot daily closing prices for the S&P500 (^GSPC)
getSymbols("^GSPC")
plot(Cl(GSPC))

# Create differenced log returns of ^GSPC
# and plot their values and correlogram
gspcrt = diff(log(Cl(GSPC)))
plot(gspcrt)
acf(gspcrt, na.action=na.omit)

# Fit an autoregressive model to ^GSPC log returns
# outputting its order and parameter estimates
gspcrt.ar <- ar(gspcrt, na.action=na.omit)
gspcrt.ar$order
gspcrt.ar$ar
