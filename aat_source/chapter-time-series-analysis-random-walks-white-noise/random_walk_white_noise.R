# Plot a correlogram of a sequence of
# normally distributed random variables
set.seed(1)
acf(rnorm(1000))

# Calculate the sample variance of a
# sequence of 1000 normally distributed
# random variables
set.seed(1)
var(rnorm(1000, mean=0, sd=1))

# Plot a realisation of a random walk
set.seed(4)
x <- w <- rnorm(1000)
for (t in 2:1000) x[t] <- x[t-1] + w[t]
plot(x, type="l")

# Plot the correlogram of the random walk
acf(x)

# Take differences of the random walk and
# plot its correlogram
acf(diff(x))

# Install quantmod
install.packages('quantmod')
require('quantmod')

# Obtain Microsoft (MSFT) daily prices from Yahoo
# and plot the differences in adjusted closing prices
getSymbols('MSFT', src='yahoo')
acf(diff(Ad(MSFT)), na.action = na.omit)

# Obtain S&P500 (^GSPC) daily prices from Yahoo
# and plot the differences in adjusted closing prices
getSymbols('^GSPC', src='yahoo')
acf(diff(Ad(GSPC)), na.action = na.omit)
