library("quantmod")
library("tseries")

## Obtain ARNC and UNG
getSymbols("ARNC", from="2014-11-11", to="2017-01-01")
getSymbols("UNG", from="2014-11-11", to="2017-01-01")

## Utilise the backwards-adjusted closing prices
aAdj = unclass(ARNC$ARNC.Adjusted)
bAdj = unclass(UNG$UNG.Adjusted)

## Plot the ETF backward-adjusted closing prices
plot(aAdj, type="l", xlim=c(0, length(aAdj)), ylim=c(0.0, 45.0), xlab="November 11th 2014 to January 1st 2017", ylab="Backward-Adjusted Prices in USD", col="blue")
par(new=T)
plot(bAdj, type="l", xlim=c(0, length(bAdj)), ylim=c(0.0, 45.0), axes=F, xlab="", ylab="", col="red")
par(new=F)

## Plot a scatter graph of the ETF adjusted prices
plot(aAdj, bAdj, xlab="ARNC Backward-Adjusted Prices", ylab="UNG Backward-Adjusted Prices")

## Carry out linear regression on the two price series
comb = lm(aAdj~bAdj)

## Now we perform the ADF test on the residuals,
## or "spread" on the model, using a single lag order
adf.test(comb$residuals, k=1)
