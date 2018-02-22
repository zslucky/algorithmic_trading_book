# Create a scatter plot of two sequences
# of normally distributed random variables
set.seed(1)
x <- seq(1,100) + 20.0*rnorm(1:100)
set.seed(2)
y <- seq(1,100) + 20.0*rnorm(1:100)
plot(x,y)

# Calculate their covariance
cov(x,y)

# Calculate their correlation
cor(x,y)

# Plot a correlogram of a sequence of
# normally distributed random variables
set.seed(1)
w <- rnorm(100)
acf(w)

# Plot a correlogram of a sequence of 
# integers from 1 to 100
w <- seq(1, 100)
acf(w)

# Plot a correlogram of a repeating
# sequence of integers from 1 to 10
w <- rep(1:10, 10)
acf(w)
