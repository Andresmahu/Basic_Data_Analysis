import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pylab as plt
from pmdarima.arima import auto_arima
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima.arima import ADFTest
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


df = pd.read_csv("data/ts_sales_months.csv")

# Get the time series
df['DATE'] = pd.to_datetime(df['TSDATE_YM'])
ts = df.loc[:, ['DATE', 'SALES']]
ts.set_index('DATE',inplace=True)

# Dickey-Fuller test
dftest = adfuller(ts)
print("Time series original without diff, we have p-value: {}".format(dftest[1]))
adf_test = ADFTest(alpha = 0.05)
print("Time series with diff, we have p-value: {}".format(adf_test.should_diff(ts)))

#           AUTO-ARIMA
#model = auto_arima(ts, start_p=0, start_q=0)
#print(model.summary())
#model.plot_diagnostics()
#plt.show()
#prediction = pd.DataFrame(model_1.predict(n_periods = 12))
#prediction.columns = ['predicted_sales']
#print(prediction)




# Fit a SARIMA model
model_1 = SARIMAX(ts.SALES, order=(0,0,0), seasonal_order=(0,1,0,12))
results = model_1.fit()
#print(results.summary())

forecast = results.get_prediction(start=-6)

mean_forecast = forecast.predicted_mean

confident_intervals = forecast.conf_int()

ts_mini = df.loc[(df.shape[0]-6):,['TSDATE_YM', 'SALES']]

lower_int = confident_intervals['lower SALES']
upper_int = confident_intervals['upper SALES']

plt.figure()
plt.plot(df.TSDATE_YM, df.SALES)
plt.plot(ts_mini.TSDATE_YM, mean_forecast.values, color='red', label='forecast')
plt.fill_between(ts_mini.TSDATE_YM, lower_int, upper_int, color='pink')
plt.gcf().autofmt_xdate()
plt.show()


