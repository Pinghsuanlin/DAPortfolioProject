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

#check if the stationary #probabily not, as we see from the plot that the mean is not constant, but we could check with Rolling Statistics or ADF test
#Determine rolling statistics
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

#or conduct ADF test
from statsmodels.tsa.statools import adfuller
print('Results of Dickey-Fuller Test:')
dftest = adfuller(indexedDf['#Passengers'], autolag='AIC') #AIC gives you information about what you want in a time series (the 

