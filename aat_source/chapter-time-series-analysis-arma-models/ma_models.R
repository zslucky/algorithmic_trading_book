# Create an MA(1) proces, plotting its values
# and correlogram, for beta_1 = 0.6
set.seed(1)
x <- w <- rnorm(100)
for (t in 2:100) x[t] <- w[t] + 0.6*w[t-1]
layout(1:2)
plot(x, type="l")
acf(x)

# Fit an ARIMA(0, 0, 1) model (i.e. MA(1) ) 
# to the series previously generated, 
# outputting its order, parameter estimates 
# and confidence intervals
x.ma <- arima(x, order=c(0, 0, 1))
0.6023 + c(-1.96, 1.96)*0.0827

# Create an MA(1) proces, plotting its values
# and correlogram, for beta_1 = -0.6
set.seed(1)
x <- w <- rnorm(100)
for (t in 2:100) x[t] <- w[t] - 0.6*w[t-1]
layout(1:2)
plot(x, type="l")
acf(x)

# Fit an ARIMA(0, 0, 1) model (i.e. MA(1) ) 
# to the series previously generated, 
# outputting its order, parameter estimates 
# and confidence intervals
x.ma <- arima(x, order=c(0, 0, 1))
-0.730 + c(-1.96, 1.96)*0.1008

# Create an MA(3) proces, plotting its values
# and correlogram, for beta_1 = 0.6, beta_2 = 0.4
# and beta_3 = 0.3
set.seed(3)
x <- w <- rnorm(1000)
for (t in 4:1000) x[t] <- w[t] + 0.6*w[t-1] + 0.4*w[t-2] + 0.3*w[t-3]
layout(1:2)
plot(x, type="l")
acf(x)

# Fit an ARIMA(0, 0, 3) model (i.e. MA(3) ) 
# to the series previously generated, 
# outputting its order, parameter estimates 
# and confidence intervals
x.ma <- arima(x, order=c(0, 0, 3))
0.544 + c(-1.96, 1.96)*0.0309
0.345 + c(-1.96, 1.96)*0.0349
0.298 + c(-1.96, 1.96)*0.0311

# Create differenced log returns of AMZN
require(quantmod)
getSymbols("AMZN")
amznrt = diff(log(Cl(AMZN)))

# Fit an ARIMA(0, 0, 1) model (i.e. MA(1) ) 
# and plot the correlogram of the residuals
amznrt.ma <- arima(amznrt, order=c(0, 0, 1))
acf(amznrt.ma$res[-1])

# Fit an ARIMA(0, 0, 2) model (i.e. MA(2) ) 
# and plot the correlogram of the residuals
amznrt.ma <- arima(amznrt, order=c(0, 0, 2))
acf(amznrt.ma$res[-1])

# Fit an ARIMA(0, 0, 3) model (i.e. MA(3) ) 
# and plot the correlogram of the residuals
amznrt.ma <- arima(amznrt, order=c(0, 0, 3))
acf(amznrt.ma$res[-1])

# Create differenced log returns 
# of the S&P500 (^GPSC)
getSymbols("^GSPC")
gspcrt = diff(log(Cl(GSPC)))

# Fit an ARIMA(0, 0, 1) model (i.e. MA(1) ) 
# and plot the correlogram of the residuals
gspcrt.ma <- arima(gspcrt, order=c(0, 0, 1))
acf(gspcrt.ma$res[-1])

# Fit an ARIMA(0, 0, 2) model (i.e. MA(2) ) 
# and plot the correlogram of the residuals
gspcrt.ma <- arima(gspcrt, order=c(0, 0, 2))
acf(gspcrt.ma$res[-1])

# Fit an ARIMA(0, 0, 3) model (i.e. MA(3) ) 
# and plot the correlogram of the residuals
gspcrt.ma <- arima(gspcrt, order=c(0, 0, 3))
acf(gspcrt.ma$res[-1])
