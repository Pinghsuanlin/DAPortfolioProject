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
indexedDataset_logScale = np.log(indexedDf)
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

df_diff_ExpDecatAvg = indexedDatset_logScale - exponentialDecayedWeightedAvg
test_stationarity(df_diff_ExpDecatAvg)
#the rolling mean and std are quite stationary, and p-value is less than 0.05

df_diff_Shifting = indexedDatset_logScale  - indexedDatset_logScale.shift()#lag of 1
plt.plot(df_diff_Shifting)

#ARIMA: AR as autoregression; I as integration; MA as moving average
df_diff_Shifting.dropna(inplace=True)
test_stationarity(df_diff_Shifting)
#it's stationary

##########Decomposition: ##########
##########Decomposition: ##########

from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(indexedDatset_logScale)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.plot(indexedDatset_logScale, leabl='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal, label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(seasonal, label='Residual')
plt.legend(loc='best')
plt.tight_layout()

#Check if the noise is stationary or not
decomposedLogData = residual
decomposedLogData .dropna(inplace=True)
test_stationarity(decomposedLogData)
#not stationary, but we have the d value (residual)


################plot ACF and PACF plots to have know the p and q value################
################plot ACF and PACF plots to have know the p and q value################
from statsmodels.tsa.stattools import acf, pacf

lag_acf = acf(df_diff_Shifting, nlags=20)
lag_pacf = pacf(df_diff_Shifting, nlags=20, method='ols')#old=ordinary least square method

#plot ACF
plt.subplot(121)
plt.plot(lag_acf)
plt.axhline(y=0,linestyle='--', color='gray')
plt.achline(y=-1.96/np.sqrt(len(df_diff_Shifting)), linestyle='--', color='gray')
plt.achline(y=1.96/np.sqrt(len(df_diff_Shifting)), linestyle='--', color='gray')
plt.title('Autocorrelation Function')

#plot PACF (partial autocorrelation graph):
plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0,linestyle='--', color='gray')
plt.achline(y=-1.96/np.sqrt(len(df_diff_Shifting)), linestyle='--', color='gray')
plt.achline(y=1.96/np.sqrt(len(df_diff_Shifting)), linestyle='--', color='gray')
plt.title('Partial Autocorrelation Function')
plt.tight_layout()
#by looking at where the value drops to 0 for the first time, you could have a rough idea on what's p and q value
#PACF: p value; ACF: q value are both around 2

#################place p, d, q to ARIMA model################
#################place p, d, q to ARIMA model################
from statsmodels.tsa.arima_model import ARIMA

#AR model
model = ARIMA(indexedDataset_logScale, order=(2,1,2))#p=2,d=1,q=2
results_AR = model.fit(disp=-1)
plt.plot(df_diff_Shifting)
plt.plot(results_AR.fittedvalues, color='red')
plt.title('RSS: %.4f'% sum((results_AR.fittedvalues-df_diff_Shifting["#Passengers"])**2))#rss as residual sum of square
print('Plotting AR model')
#Goal: min RSS

#take moving average into consideration
model= ARIMA(indexedDataset_logScale, order = (2,1,2))
results_ARIMA = model.fit(disp=-1)
plt.plot(df_diff_Shifting)
plt.plot(results_ARIMA.fittedvalues, color='red')
plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-df_diff_Shifting["#Passengers"])**2))#rss as residual sum of square
print('Plotting AR model')
#reach the best model confirmed

##################predict on time series#################
##################predict on time series#################
pred_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
print(pred_ARIMA_diff .head())

#find the cumulative sum
#convert to cumulative sum
pred_ARIMA_diff_cumsum = pred_ARIMA_diff.cumsum()
print(pred_ARIMA_diff_cumsum .head())

pred_ARIMA_log = pd.Series(indexedDataset_logScale['#Passengers'].ix[0], index=indexedDataset_logScale.index)
pred_ARIMA_log = pred_ARIMA_log.add(pred_ARIMA_diff_cumsum, fill_value=0)
pred_ARIMA_log.head()

#take the exponential value to go back to the original data
pred_ARIMA = np.exp(pred_ARIMA_log)
plt.plot(indexedDataset)
plt.plot(pred_ARIMA)

#view the dataset
indexedDataset_logScale#144 rows, 1 variable

#predict for the next ten years (144+120)
results_ARIMA.plot_predict(1,264)
x=results_ARIMA.forecast(steps=120)#to get the exact data point




