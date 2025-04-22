# Load necessary libraries
library(ggplot2)
library(forecast)
library(tseries)
library(faraway)

# Open a new plotting window
x11()

# Read the CSV file
df <- read.csv("bitcoin_univariate.csv")

# Convert Date column to Date type
df$Date <- as.Date(df$Date)

# Select the last 75 months (~2250 days assuming daily data)
df_sample <- tail(df, 75 * 30)

# Find the optimal lambda for Box-Cox transformation
lambda <- BoxCox.lambda(df_sample$Close)

# Apply Box-Cox transformation
df_sample$Close_transformed <- BoxCox(df_sample$Close, lambda)

# Perform first-order differencing
df_sample$Close_diff <- c(NA, diff(df_sample$Close_transformed))

# Remove NA from differenced series
diff_series <- na.omit(df_sample$Close_diff)

# ADF test for stationarity
adf_result <- adf.test(diff_series)
print(adf_result)

# Fit the best ARIMA model automatically
arima_model <- arima(df_sample$Close_transformed, order = c(1,1,2))

# Print ARIMA model summary
print(arima_model)

# Extract standardized residuals
std_residuals <- residuals(arima_model) / sd(residuals(arima_model))

# Open new window for residual diagnostics
x11()
par(mfrow = c(2,2))

# Residuals Histogram
hist(std_residuals, breaks = 30, col = "lightblue", main = "Standardized Residuals Histogram", 
     xlab = "Standardized Residuals", probability = TRUE)
lines(density(std_residuals), col = "red", lwd = 2)

# Q-Q Plot
qqnorm(std_residuals, main = "Q-Q Plot of Standardized Residuals")
qqline(std_residuals, col = "red", lwd = 2)

# ACF of residuals
acf(std_residuals, main = "Autocorrelation of Standardized Residuals")

# Ljung-Box Test (for autocorrelation)
ljung_test <- Box.test(std_residuals, lag = 20, type = "Ljung-Box")
print(ljung_test)

# Runs Test (for randomness) - FIXED!
runs_test <- runs.test(factor(std_residuals > 0))
print(runs_test)

# Shapiro-Wilk Test (for normality)
shapiro_test <- shapiro.test(std_residuals)
print(shapiro_test)
