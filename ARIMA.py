import pandas as pd 
from pandas import Series
from statsmodels.tsa.arima_model import ARIMA
import numpy
 
# create a differenced series
def difference(dataset, interval=1):
  diff = list()
  for i in range(interval, len(dataset)):
    value = dataset[i] - dataset[i - interval]
    diff.append(value)
  return numpy.array(diff)
 
# invert differenced value
def inverse_difference(history, yhat, interval=1):
  return yhat + history[-interval]
 

if __name__ == "__main__":
  code = 2127
  # load dataset
  df = pd.read_csv("csv/{}.csv".format(code), index_col="date")
  # seasonal difference 
  X = df.close.values

  days_in_year = 30
  differenced = difference(X, days_in_year)
  # fit model
  model = ARIMA(differenced, order=(5,0,1))
  model_fit = model.fit(disp=0)

  # one-step out-of sample forecast
  #forecasts = model_fit.forecast(steps=7)
  #forecast = forecasts[0]
  #print('1 Forecast: {}, last real data:{}'.format(forecast, df.close[-1]))
  
  # invert the differenced forecast to something usable
  #forecast = inverse_difference(X, forecast, days_in_year)
  
  start_index = len(differenced)
  end_index = start_index + 4
  forecast = model_fit.predict(start=start_index, end=end_index)
  #print('2 Forecast: {}, last real data:{}'.format(forecast, df.close[-1]))

  history = [x for x in X]
  day = 1
  for yhat in forecast:
        inverted = inverse_difference(history, yhat,days_in_year)
        print('Day %d:%f' % (day, inverted))
        history.append(inverted)
        day += 1

  