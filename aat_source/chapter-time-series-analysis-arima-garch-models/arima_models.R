# Simulate an ARIMA(1,1,1) model with alpha = 0.6
# and beta = 0.5, then plot the values
set.seed(2)
x <- arima.sim(list(order = c(1,1,1), ar = 0.6, ma=-0.5), n = 1000)
plot(x)

# Fit an ARIMA(1,1,1) model to the realisation above
# and calculate confidence intervals
x.arima <- arima(x, order=c(1, 1, 1))
0.6470 + c(-1.96, 1.96)*0.1065
-0.5165 + c(-1.96, 1.96)*0.1189

# Plot the residuals of the fitted model
acf(resid(x.arima))

# Calculate the Ljung-Box test
Box.test(resid(x.arima), lag=20, type="Ljung-Box")

# Install the forecast library
install.packages("forecast")
library(forecast)

# Obtain differenced log prices for AMZN
require(quantmod)
getSymbols("AMZN", from="2013-01-01")
amzn = diff(log(Cl(AMZN)))

# Calculate the best fitting ARIMA model
azfinal.aic <- Inf
azfinal.order <- c(0,0,0)
for (p in 1:4) for (d in 0:1) for (q in 1:4) {
  azcurrent.aic <- AIC(arima(amzn, order=c(p, d, q)))
  if (azcurrent.aic < azfinal.aic) {
    azfinal.aic <- azcurrent.aic
    azfinal.order <- c(p, d, q)
    azfinal.arima <- arima(amzn, order=azfinal.order)
  }
}

# Output the best ARIMA order
azfinal.order

# Plot a correlogram of the residuals, calculate 
# the Ljung-Box test and predict the next 25 daily
# values of the series
acf(resid(azfinal.arima), na.action=na.omit)
Box.test(resid(azfinal.arima), lag=20, type="Ljung-Box")
plot(forecast(azfinal.arima, h=25))

# Obtain differenced log prices for the S&P500
getSymbols("^GSPC", from="2013-01-01")
sp = diff(log(Cl(GSPC)))

# Calculate the best fitting ARIMA model
spfinal.aic <- Inf
spfinal.order <- c(0,0,0)
for (p in 1:4) for (d in 0:1) for (q in 1:4) {
  spcurrent.aic <- AIC(arima(sp, order=c(p, d, q)))
  if (spcurrent.aic < spfinal.aic) {
    spfinal.aic <- spcurrent.aic
    spfinal.order <- c(p, d, q)
    spfinal.arima <- arima(sp, order=spfinal.order)
  }
}

# Output the best ARIMA order
spfinal.order

# Plot a correlogram of the residuals, calculate 
# the Ljung-Box test and predict the next 25 daily
# values of the series
acf(resid(spfinal.arima), na.action=na.omit)
Box.test(resid(spfinal.arima), lag=20, type="Ljung-Box")
plot(forecast(spfinal.arima, h=25))
