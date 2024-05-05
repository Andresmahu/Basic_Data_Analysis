library(tseries)
library(ggplot2)
library(forecast)

# Test
library(nortest)
library(FinTS)

df1 <- read.csv("C:/Users/maste/Desktop/Data_Science/Basic_Data_Analysis/data/ts_sales_months.csv")

df1$SALES <- df1$SALES/1000
serie <- ts(df1$SALES, start = c(2003, 1), frequency = 12)

# Original
#par(mar=c(1,1,1,1))
plot(serie,  
     col = "mediumturquoise", 
     main = "Serie de Tiempo", 
     xlab= "Years",
     ylab = "Sales in K")


# Plot with no tendency
seriet <- diff(serie,lag=1,differences = 1)
par(mar=c(1,1,1,1))
plot(seriet, col = "coral", main = "Serie")

# Hypothesis testing
k<-trunc(length(df1$SALES)^(1/4))
adf.test(seriet,k=k)

# p & q
#p
pacf(seriet, lag.max=30, main = "PACF", col = "firebrick4")

#q
acf(seriet, lag.max=30, main = "ACF", col ="firebrick4")
#q = 1,3,9


auto_model <- auto.arima(serie)
print(forecast(auto_model, h=12))
#par(mar=c(1,1,1,1))
plot(forecast(auto_model,h=12),
     type  ="l", 
     col = "lightseagreen", 
     main = "Predicciones",
     xlab= "Years",
     ylab = "Sales in K",
     axes=TRUE)

print(summary(auto_model))


# Assumptions verification


# Test Ljung-Box, where h0: No autocorrelation
Box.test(auto_model$residuals, type = "Ljung-Box")

# Test ArchText, where h0: Constant variance
ArchTest(auto_model$residuals)

# Test t, where h0: mean = 0
t.test(auto_model$residuals)

# Test Lilliefors, where h0: e~Normal
lillie.test(auto_model$residuals)






















