#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___
# <center>*Copyright Pierian Data 2017*</center>
# <center>*For more information, visit us at www.pieriandata.com*</center>

# # Rolling and Expanding
# 
# A very common process with time series is to create data based off of a rolling mean. 
# Let's show you how to do this easily with pandas!
import pandas as pd
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/8_time_series/figs/'
# Best way to read in data with time series index!
df = pd.read_csv('time_data/walmart_stock.csv',index_col='Date',parse_dates=True)
print(df.head())

df['Open'].plot(figsize=(16,6))
plt.savefig(PATH + 'walmart_stock.png', dpi=300)
plt.close()


# Now let's add in a rolling mean! This rolling method provides row entries, 
# where every entry is then representative of the window. 
# 7 day rolling mean
print(df.rolling(7).mean().head(20))
df['Open'].plot()
df.rolling(window=30).mean()['Close'].plot()
plt.savefig(PATH + 'walmart_close_rolling.png', dpi=300)
plt.close()

# Easiest way to add a legend is to make this rolling value a new column, 
# then pandas does it automatically!
df['Close: 30 Day Mean'] = df['Close'].rolling(window=30).mean()
df[['Close','Close: 30 Day Mean']].plot(figsize=(16,6))
plt.savefig(PATH + 'walmart_ma.png', dpi=300)
plt.close()

# ## expanding
# 
# Now what if you want to take into account everything from the 
# start of the time series as a rolling value? For instance, not just take 
# into account a period of 7 days, or monthly rolling average, but instead, 
# take into everything since the beginning of the time series, continuously:
# Optional specify a minimum number of periods
df['Close'].expanding(min_periods=1).mean().plot(figsize=(16,6))
plt.savefig(PATH + 'walmart_expanding.png', dpi=300)
plt.close()

# ## Bollinger Bands
# 
# We will talk a lot more about financial analysis plots and technical indicators,
# but here is one worth mentioning!
# 
# More info : http://www.investopedia.com/terms/b/bollingerbands.asp
# 
# *Developed by John Bollinger, Bollinger Bands® are volatility bands placed above
# and below a moving average. Volatility is based on the standard deviation, 
# which changes as volatility increases and decreases. The bands automatically 
# widen when volatility increases and narrow when volatility decreases. This 
# dynamic nature of Bollinger Bands also means they can be used on different 
# securities with the standard settings. For signals, Bollinger Bands can be 
# used to identify Tops and Bottoms or to determine the strength of the trend.*
# 
# *Bollinger Bands reflect direction with the 20-period SMA and volatility with 
# the upper/lower bands. As such, they can be used to determine if prices are
# relatively high or low. According to Bollinger, the bands should contain 
# 88-89% of price action, which makes a move outside the bands significant. 
# Technically, prices are relatively high when above the upper band and 
# relatively low when below the lower band. However, relatively high should 
# not be regarded as bearish or as a sell signal. Likewise, relatively low should 
# not be considered bullish or as a buy signal. Prices are high or low for a 
# reason. As with other indicators, Bollinger Bands are not meant to be used 
# as a stand alone tool. *
df['Close: 30 Day Mean'] = df['Close'].rolling(window=20).mean()
df['Upper'] = df['Close: 30 Day Mean'] + 2*df['Close'].rolling(window=20).std()
df['Lower'] = df['Close: 30 Day Mean'] - 2*df['Close'].rolling(window=20).std()
df[['Close','Close: 30 Day Mean','Upper','Lower']].plot(figsize=(16,6))
plt.savefig(PATH + 'bollinger.png', dpi=300)
plt.close()
# For expanding operations, it doesn't help very much to visualize 
# this against the daily data, but instead its a good way to get an 
# idea of the "stability" of a stock. This idea of stability and volatility 
# is something we are going to be exploring heavily in the next project, so 
# let's jump straight into it!
