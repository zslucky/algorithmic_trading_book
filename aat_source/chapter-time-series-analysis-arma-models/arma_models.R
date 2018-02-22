# Simulate an ARMA(1,1) model with alpha = 0.5 and 
# beta = 0.5, then plot its values and correlogram
set.seed(1)
x <- arima.sim(n=1000, model=list(ar=0.5, ma=-0.5))
plot(x)
acf(x)

# Determine the parameters and calculate confidence
# intervals using the arima function
arima(x, order=c(1, 0, 1))
-0.396 + c(-1.96, 1.96)*0.373
0.450 + c(-1.96, 1.96)*0.362

# Simulate an ARMA(2,2) model with alpha_1 = 0.5,
# alpha_2 = -0.25, beta_1 = 0.5 and beta_2 = -0.3 
# then plot its values and correlogram
set.seed(1)
x <- arima.sim(n=1000, model=list(ar=c(0.5, -0.25), ma=c(0.5, -0.3)))
plot(x)
acf(x)

# Determine the parameters and calculate confidence
# intervals using the arima function
arima(x, order=c(2, 0, 2))
0.653 + c(-1.96, 1.96)*0.0802
-0.229 + c(-1.96, 1.96)*0.0346
0.319 + c(-1.96, 1.96)*0.0792
-0.552 + c(-1.96, 1.96)*0.0771

# Create an ARMA(3,2) model
set.seed(3)
x <- arima.sim(n=1000, model=list(ar=c(0.5, -0.25, 0.4), ma=c(0.5, -0.3)))

# Loop over p = 0 to 4, q = 0 to 4 and create each
# ARMA(p,q) model, then fit to the previous ARMA(3,2)
# realisation, using the AIC to find the best fit
final.aic <- Inf
final.order <- c(0,0,0)
for (i in 0:4) for (j in 0:4) {
  current.aic <- AIC(arima(x, order=c(i, 0, j)))
  if (current.aic < final.aic) {
    final.aic <- current.aic
    final.order <- c(i, 0, j)
    final.arma <- arima(x, order=final.order)
  }
}

# Output the results of the fit
final.aic
final.order
final.arma

# Plot the residuals of the final model
acf(resid(final.arma))

# Carry out a Ljung-Box test for realisation
# of discrete white noise
Box.test(resid(final.arma), lag=20, type="Ljung-Box")

# Create S&P500 differenced log returns
require(quantmod)
getSymbols("^GSPC")
sp = diff(log(Cl(GSPC)))

# Loop over p = 0 to 4, q = 0 to 4 and create each
# ARMA(p,q) model, then fit to the previous S&P500 
# returns, using the AIC to find the best fit
spfinal.aic <- Inf
spfinal.order <- c(0,0,0)
for (i in 0:4) for (j in 0:4) {
  spcurrent.aic <- AIC(arima(sp, order=c(i, 0, j)))
  if (spcurrent.aic < spfinal.aic) {
    spfinal.aic <- spcurrent.aic
    spfinal.order <- c(i, 0, j)
    spfinal.arma <- arima(sp, order=spfinal.order)
  }
}

# Output the results of the fit
spfinal.order

# Plot the residuals of the final model
acf(resid(spfinal.arma), na.action=na.omit)

# Carry out a Ljung-Box test for realisation
# of discrete white noise
Box.test(resid(spfinal.arma), lag=20, type="Ljung-Box")
