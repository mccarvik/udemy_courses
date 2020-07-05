#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___
# <center>*Copyright Pierian Data 2017*</center>
# <center>*For more information, visit us at www.pieriandata.com*</center>

# #### Warning! This is a complicated topic! Remember that this is an optional 
# notebook to go through and that to fully understand it you should read the 
# supplemental links and watch the full explanatory walkthrough video. This notebook 
# and the video lectures are not meant to be a full comprehensive overview of ARIMA, 
# but instead a walkthrough of what you can use it for, so you can later understand 
# why it may or may not be a good choice for Financial Stock Data.
# ____
# 
# 
# # ARIMA and Seasonal ARIMA
# 
# 
# ## Autoregressive Integrated Moving Averages
# 
# The general process for ARIMA models is the following:
# * Visualize the Time Series Data
# * Make the time series data stationary
# * Plot the Correlation and AutoCorrelation Charts
# * Construct the ARIMA Model
# * Use the model to make predictions
# 
# Let's go through these steps!

# ## Step 1: Get the Data (and format it)
# 
# We will be using some data about monthly milk production, full details on it can be 
# found [here](https://datamarket.com/data/set/22ox/monthly-milk-production-pounds-per-cow-jan-62-dec-75#!ds=22ox&display=line).
# 
# Its saved as a csv for you already, let's load it up:
import pdb, sys
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/10_time_series_analysis/figs/'
df = pd.read_csv('monthly-milk-production-pounds-p.csv')
print(df.head())
print(df.tail())

# ** Clean Up**
# 
# Let's clean this up just a little!
df.columns = ['Month','Milk in pounds per cow']
print(df.head())

# Weird last value at bottom causing issues
df.drop(168,axis=0,inplace=True)
df['Month'] = pd.to_datetime(df['Month'])
print(df.head())
df.set_index('Month',inplace=True)
print(df.head())
print(df.describe().transpose())

# ## Step 2: Visualize the Data
# 
# Let's visualize this data with a few methods.
df.plot()
plt.savefig(PATH + 'milk.png', dpi=300)
plt.close()

timeseries = df['Milk in pounds per cow']
timeseries.rolling(12).mean().plot(label='12 Month Rolling Mean')
timeseries.rolling(12).std().plot(label='12 Month Rolling Std')
timeseries.plot()
plt.legend()
plt.savefig(PATH + 'milk_time_series.png', dpi=300)
plt.close()

timeseries.rolling(12).mean().plot(label='12 Month Rolling Mean')
timeseries.plot()
plt.legend()
plt.savefig(PATH + 'milk_12m.png', dpi=300)
plt.close()

# ## Decomposition
# 
# ETS decomposition allows us to see the individual parts!

from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(df['Milk in pounds per cow'], freq=12)  
fig = plt.figure()  
fig = decomposition.plot()  
fig.set_size_inches(15, 8)
plt.savefig(PATH + 'milk_ets.png', dpi=300)
plt.close()

# ## Testing for Stationarity
# 
# We can use the Augmented [Dickey-Fuller](https://en.wikipedia.org/wiki/Augmented_Dickey%E2%80%93Fuller_test) [unit root test](https://en.wikipedia.org/wiki/Unit_root_test).
# 
# In statistics and econometrics, an augmented Dickey–Fuller test (ADF) tests the 
# null hypothesis that a unit root is present in a time series sample. The alternative 
# hypothesis is different depending on which version of the test is used, but is 
# usually stationarity or trend-stationarity.
# 
# Basically, we are trying to whether to accept the Null Hypothesis **H0** (that 
# the time series has a unit root, indicating it is non-stationary) or reject **H0** 
# and go with the Alternative Hypothesis (that the time series has no unit root and 
# is stationary).
# 
# We end up deciding this based on the p-value return.
# 
# * A small p-value (typically ≤ 0.05) indicates strong evidence against the null 
# hypothesis, so you reject the null hypothesis.
# 
# * A large p-value (> 0.05) indicates weak evidence against the null hypothesis,
# so you fail to reject the null hypothesis.
# 
# Let's run the Augmented Dickey-Fuller test on our data:
print(df.head())
from statsmodels.tsa.stattools import adfuller
result = adfuller(df['Milk in pounds per cow'])
print('Augmented Dickey-Fuller Test:')
labels = ['ADF Test Statistic','p-value','#Lags Used','Number of Observations Used']

for value,label in zip(result,labels):
    print(label+' : '+str(value) )
    
if result[1] <= 0.05:
    print("strong evidence against the null hypothesis, reject the null hypothesis. Data has no unit root and is stationary")
else:
    print("weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")

# Store in a function for later use!
def adf_check(time_series):
    """
    Pass in a time series, returns ADF report
    """
    result = adfuller(time_series)
    print('Augmented Dickey-Fuller Test:')
    labels = ['ADF Test Statistic','p-value','#Lags Used','Number of Observations Used']

    for value,label in zip(result,labels):
        print(label+' : '+str(value) )
    
    if result[1] <= 0.05:
        print("strong evidence against the null hypothesis, reject the null hypothesis. Data has no unit root and is stationary")
    else:
        print("weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")

# ___________
# 
# ## Important Note!
# 
# ** We have now realized that our data is seasonal (it is also pretty obvious from the plot 
# itself). This means we need to use Seasonal ARIMA on our model. If our data was not 
# seasonal, it means we could use just ARIMA on it. We will take this into account 
# when differencing our data! Typically financial stock data won't be seasonal, 
# but that is kind of the point of this section, to show you common methods, that 
# won't work well on stock finance data!**
# 
# _____

# ## Differencing
# 
# The first difference of a time series is the series of changes from one period 
# to the next. We can do this easily with pandas. You can continue to take the 
# second difference, third difference, and so on until your data is stationary.
# ** First Difference **
df['Milk First Difference'] = df['Milk in pounds per cow'] - df['Milk in pounds per cow'].shift(1)
adf_check(df['Milk First Difference'].dropna())
df['Milk First Difference'].plot()
plt.savefig(PATH + 'milk_first_diff.png', dpi=300)
plt.close()

# ** Second Difference **
# Sometimes it would be necessary to do a second difference 
# This is just for show, we didn't need to do a second difference in our case
df['Milk Second Difference'] = df['Milk First Difference'] - df['Milk First Difference'].shift(1)
adf_check(df['Milk Second Difference'].dropna())
df['Milk Second Difference'].plot()
plt.savefig(PATH + 'milk_sec_diff.png', dpi=300)
plt.close()

# ** Seasonal Difference **
df['Seasonal Difference'] = df['Milk in pounds per cow'] - df['Milk in pounds per cow'].shift(12)
df['Seasonal Difference'].plot()
plt.savefig(PATH + 'milk_seasonal_diff.png', dpi=300)
plt.close()

# Seasonal Difference by itself was not enough!
adf_check(df['Seasonal Difference'].dropna())

# ** Seasonal First Difference **
# You can also do seasonal first difference
df['Seasonal First Difference'] = df['Milk First Difference'] - df['Milk First Difference'].shift(12)
df['Seasonal First Difference'].plot()
plt.savefig(PATH + 'milk_seasonal_first_diff.png', dpi=300)
plt.close()
adf_check(df['Seasonal First Difference'].dropna())

# # Autocorrelation and Partial Autocorrelation Plots
# 
# An autocorrelation plot (also known as a [Correlogram](https://en.wikipedia.org/wiki/Correlogram) ) shows the correlation of the series with itself, lagged by x time units. So the y axis is the correlation and the x axis is the number of time units of lag.
# 
# So imagine taking your time series of length T, copying it, and deleting the 
# first observation of copy #1 and the last observation of copy #2. Now you have 
# two series of length T−1 for which you calculate a correlation coefficient. 
# This is the value of of the vertical axis at x=1x=1 in your plots. It represents 
# the correlation of the series lagged by one time unit. You go on and do this 
# for all possible time lags x and this defines the plot.
# 
# You will run these plots on your differenced/stationary data. There is a lot 
# of great information for identifying and interpreting ACF and PACF [here](http://people.duke.edu/~rnau/arimrule.htm) and [here](https://people.duke.edu/~rnau/411arim3.htm).
# 
# ### Autocorrelation Interpretation
# 
# The actual interpretation and how it relates to ARIMA models can get a bit 
# complicated, but there are some basic common methods we can use for the ARIMA model. 
# Our main priority here is to try to figure out whether we will use the AR or MA 
# components for the ARIMA model (or both!) as well as how many lags we should use. 
# In general you would use either AR or MA, using both is less common.
# 
# * If the autocorrelation plot shows positive autocorrelation at the first lag (lag-1),
# then it suggests to use the AR terms in relation to the lag
# 
# * If the autocorrelation plot shows negative autocorrelation at the first lag, 
# then it suggests using MA terms.

# _____
# ### <font color='red'> Important Note! </font> 
# 
# Here we will be showing running the ACF and PACF on multiple differenced data 
# sets that have been made stationary in different ways, typically you would just 
# choose a single stationary data set and continue all the way through with that.
# 
# The reason we use two here is to show you the two typical types of behaviour 
# you would see when using ACF.
# _____
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
# Duplicate plots
# Check out: https://stackoverflow.com/questions/21788593/statsmodels-duplicate-charts
# https://github.com/statsmodels/statsmodels/issues/1265
fig_first = plot_acf(df["Milk First Difference"].dropna())
plt.savefig(PATH + 'milk_acf.png', dpi=300)
plt.close()

fig_seasonal_first = plot_acf(df["Seasonal First Difference"].dropna())
plt.savefig(PATH + 'milk_acf_seasonal.png', dpi=300)
plt.close()

# Pandas also has this functionality built in, but only for ACF, not PACF. So I 
# recommend using statsmodels, as ACF and PACF is more core to its functionality 
# than it is to pandas' functionality.
from pandas.plotting import autocorrelation_plot
autocorrelation_plot(df['Seasonal First Difference'].dropna())
plt.savefig(PATH + 'milk_autocorr.png', dpi=300)
plt.close()

# ## Partial Autocorrelation
# 
# In general, a partial correlation is a conditional correlation.
# 
# It is the correlation between two variables under the assumption that we know 
# and take into account the values of some other set of variables.
# 
# For instance, consider a regression context in which y = response variable and 
# x1, x2, and x3 are predictor variables.  The partial correlation between y and 
# x3 is the correlation between the variables determined taking into account how 
# both y and x3 are related to x1 and x2.
# 
# Formally, this is relationship is defined as:
# 
# ## $\frac{\text{Covariance}(y, x_3|x_1, x_2)}{\sqrt{\text{Variance}(y|x_1, x_2)\text{Variance}(x_3| x_1, x_2)}}$
# 
# Check out this [link](http://www.itl.nist.gov/div898/handbook/pmc/section4/pmc4463.htm) for full details on this.

# We can then plot this relationship:
pdb.set_trace()
result = plot_pacf(df["Seasonal First Difference"].dropna(), method='ywmle')
plt.savefig(PATH + 'milk_pacf.png', dpi=300)
plt.close()
sys.exit()

# ### Interpretation
# 
# Typically a sharp drop after lag "k" suggests an AR-k model should be used. 
# If there is a gradual decline, it suggests an MA model.

# ### Final Thoughts on Autocorrelation and Partial Autocorrelation
# 
# * Identification of an AR model is often best done with the PACF.
#     * For an AR model, the theoretical PACF “shuts off” past the order of the model. 
#       The phrase “shuts off” means that in theory the partial autocorrelations 
#       are equal to 0 beyond that point.  Put another way, the number of non-zero 
#       partial autocorrelations gives the order of the AR model.  By the “order of the 
#       model” we mean the most extreme lag of x that is used as a predictor.
#     
#     
# * Identification of an MA model is often best done with the ACF rather than the PACF.
#     * For an MA model, the theoretical PACF does not shut off, but instead tapers 
#       toward 0 in some manner.  A clearer pattern for an MA model is in the ACF.  
#       The ACF will have non-zero autocorrelations only at lags involved in the model.

# _____
# ### Final ACF and PACF Plots
# 
# We've run quite a few plots, so let's just quickly get our "final" ACF and PACF plots. 
# These are the ones we will be referencing in the rest of the notebook below.
# _____
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(df['Seasonal First Difference'].iloc[13:], lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(df['Seasonal First Difference'].iloc[13:], lags=40, ax=ax2)


# ## Using the Seasonal ARIMA model
# 
# Finally we can use our ARIMA model now that we have an understanding of our data!

# In[38]:


# For non-seasonal data
from statsmodels.tsa.arima_model import ARIMA


# In[39]:


# I recommend you glance over this!

# 
help(ARIMA)


# ### p,d,q parameters
# 
# * p: The number of lag observations included in the model.
# * d: The number of times that the raw observations are differenced, also called the degree of differencing.
# * q: The size of the moving average window, also called the order of moving average.

# In[55]:


# We have seasonal data!
model = sm.tsa.statespace.SARIMAX(df['Milk in pounds per cow'],order=(0,1,0), seasonal_order=(1,1,1,12))
results = model.fit()
print(results.summary())


# In[41]:


results.resid.plot()


# In[42]:


results.resid.plot(kind='kde')


# ## Prediction of Future Values
# 
# Firts we can get an idea of how well our model performs by just predicting for values that we actually already know:

# In[43]:


df['forecast'] = results.predict(start = 150, end= 168, dynamic= True)  
df[['Milk in pounds per cow','forecast']].plot(figsize=(12,8))


# ### Forecasting
# This requires more time periods, so let's create them with pandas onto our original dataframe!

# In[44]:


print(df.tail())


# In[45]:


# https://pandas.pydata.org/pandas-docs/stable/timeseries.html
# Alternatives 
# pd.date_range(df.index[-1],periods=12,freq='M')
from pandas.tseries.offsets import DateOffset
future_dates = [df.index[-1] + DateOffset(months=x) for x in range(0,24) ]
print(future_dates)
future_dates_df = pd.DataFrame(index=future_dates[1:],columns=df.columns)
future_df = pd.concat([df,future_dates_df])

print(future_df.head())
print(future_df.tail())

future_df['forecast'] = results.predict(start = 168, end = 188, dynamic= True)  
future_df[['Milk in pounds per cow', 'forecast']].plot(figsize=(12, 8)) 
