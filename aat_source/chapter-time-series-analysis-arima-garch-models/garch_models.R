# Create a GARCH(1,1) model, with alpha_0 = 0.2,
# alpha_1 = 0.5 and beta_1 = 0.3
set.seed(2)
a0 <- 0.2
a1 <- 0.5
b1 <- 0.3
w <- rnorm(10000)
eps <- rep(0, 10000)
sigsq <- rep(0, 10000)
for (i in 2:10000) {
  sigsq[i] <- a0 + a1 * (eps[i-1]^2) + b1 * sigsq[i-1]
  eps[i] <- w[i]*sqrt(sigsq[i])
}

# Plot the correlograms of both the residuals
# and the squared residuals
acf(eps)
acf(eps^2)

# Include the tseries time series library
require(tseries)

# Fit a GARCH model to the series and calculate 
# confidence intervals for the parameters at the 
# 97.5% level
eps.garch <- garch(eps, trace=FALSE)
confint(eps.garch)

# Obtain the differenced log values of the FTSE100
# and plot the values
require(quantmod)
getSymbols("^FTSE")
ftrt = diff(log(Cl(FTSE)))
plot(ftrt)

# Remove the NA value created by the diff procedure
ft <- as.numeric(ftrt)
ft <- ft[!is.na(ft)]

# Fit a suitable ARIMA(p,d,q) model to the 
# FTSE100 returns series
ftfinal.aic <- Inf
ftfinal.order <- c(0,0,0)
for (p in 1:4) for (d in 0:1) for (q in 1:4) {
  ftcurrent.aic <- AIC(arima(ft, order=c(p, d, q)))
  if (ftcurrent.aic < ftfinal.aic) {
    ftfinal.aic <- ftcurrent.aic
    ftfinal.order <- c(p, d, q)
    ftfinal.arima <- arima(ft, order=ftfinal.order)
  }
}

# Output the order of the fit
ftfinal.order

# Plot both the residuals and the squared residuals
acf(resid(ftfinal.arima))
acf(resid(ftfinal.arima)^2)

# Fit a GARCH model
ft.garch <- garch(ft, trace=F)
ft.res <- ft.garch$res[-1]

# Plot the residuals and squared residuals
acf(ft.res)
acf(ft.res^2)
