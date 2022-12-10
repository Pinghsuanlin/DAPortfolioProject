#Goal: Build a model to forecast the demand (passenger traffic) in Airplanes
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
%matplotlib inline
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 10, 6


df = pd.read_csv("Passengers.csv")
#Parse strings to datetime type
dataset['Month'] = pd.to_datetime(df['Month'], infer_datetime_format=True)
indexedDf = df.set_index(['Month'])
indexedDf.head(5) 


# plot graph
plt.xlabel("Date")
plt.ylabel("Number of air passengers")
plt.plot(indexedDf )


########check if the stationary #probabily not, as we see from the plot that the mean is not constant, ########
########but we could check with Rolling Statistics or ADF test########

#########1. Determine rolling statistics
rolmean=indexedDf.rolling(window=12).mean() #window of 12 month
rolstd = indexedDf.rolling(window=12).std() 
print(rolmean, rolstd)
#the first 11 months would be na, as the window is 12

#plot the rolling statistics
orig. = plt.plot(indexedDf, color= 'blue', label= 'Original')
mean = plt.plot(rolmean, color='red', label = 'Rolling Mean')
std = plt.plot(rolstd, color='black', label= 'Rolling Std')
plt.legend(loc='best')
plt.title('Rolling Mean & Standard Deviation')
plt.show(block= False)
#you can see that mean and std is not standard, so it's not stationary

#########2. conduct ADF test
from statsmodels.tsa.statools import adfuller
print('Results of Dickey-Fuller Test:')
dftest = adfuller(indexedDf['#Passengers'], autolag='AIC') #AIC gives you information about how well a model fits the data
# In statistics, AIC is used to compare different possible models and determine which one is the best fit for the data. 
# If a model is more than 2 AIC units lower than another, then it is considered significantly better than that model.

dfoutput = pd.Series(dftest[0:4], index=['Test Statistics', 'p-value', '#Lags Used', 'Number of Observations Used'])
for key, value in dftest[4].items():
dfoutput['Critical Value (%s)' %key]= value
print(dfoutput)
#If p-value is more than 0.05, or if test statistics is higher thant critical value, we don't reject null hypothesis; ie the data is non-stationary

##########Estimate trend: ##########
##########Estimate trend: ##########

#taking the log of the data trend
indexedDataset_logScale = np.log(indexedDataset)
plt.plot(indexedDatset_logScale)

#Calculate the moving average of the same window
movingAverage = indexedDataset_logScale.rolling(window=12).mean()
movingSTD = indexedDataset_logScale.rolling(window=12).std()
plt.plot(indexedDataset_logScale)
plt.plot(movingAverage, color='red')
#if the mean is still moving with time, it's not stationary

#get the difference between moving average and the actual number of passengers
df_diff = indexedDatset_logScale - movingAverage
df_diff.head(12)

#remove nan values
df_diff.dropna(inplace=True)
df_diff.head(10)

#Create function
from statsmodels.tsa.stattools import adfuller
def test_stationarity(timeseries):
  #Determing rolling statistics
  movingAverage = timeseries.rolling(window=12).mean()
  movingSTD = timeseries.rolling(window=12).std()

  #plot rolling statistics:
  orig = plt.plot(timeseries, color='blue', label='Original')
  mean = plt.plot(movingAverage, color='red', label='Rolling Mean')
  std = plt.plot(movingSTD, color='black', label ='Rolling Std')
  plt.legend(loc='best')
  plt.title('Rolling Mean & Standard Deviation')
  plt.show(block=False)

  #perform Dickey-Fuller test:
  print('Results of Dickey-Fuller Test:')
  dftest = adfuller(timeseries['#Passengers'], autolag='AIC')
  dfoutput = pd.Serie(dftest[0:4], index=['Test Statistics', 'p-value', '#Lags Used', 'Number of Observations Used'])
  for key, value in dftest[4].items():
    dfoutput['Critical Value (%s)' %key] = value
  print(dfoutput)

test_stationarity(df_diff)
#kind of stationary

exponentialDecayedWeightedAvg = indexedDataset_logScale.ewm(halflife=12, min_periods=0, adjust=True).mean()
plt.plot(indexedDataset_logScale)
plt.plot(exponentialDecayedWeightedAvg, color='red')



