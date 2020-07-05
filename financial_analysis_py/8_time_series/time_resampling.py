#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___
# <center>*Copyright Pierian Data 2017*</center>
# <center>*For more information, visit us at www.pieriandata.com*</center>

# # Time Resampling
# 
# Let's learn how to sample time series data! This will be useful later on in the course!
import sys, pdb
import numpy as np
import pandas as pd
# get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/8_time_series/figs/'
# Grab data
# Faster alternative
# df = pd.read_csv('time_data/walmart_stock.csv',index_col='Date')
df = pd.read_csv('time_data/walmart_stock.csv')
print(df.head())

# Create a date index from the date column
df['Date'] = df['Date'].apply(pd.to_datetime)
print(df.head())

df.set_index('Date',inplace=True)
print(df.head())

# ## resample()
# 
# A common operation with time series data is resamplling based on the time series
# index. Let see how to use the resample() method.
# 
# #### All possible time series offest strings

# business day frequency
# custom business day frequency (experimental)
# calendar day frequency
# weekly frequency
# month end frequency
# semi-month end frequency (15th and end of month)
# business month end frequency
# custom business month end frequency
# month start frequency
# semi-month start frequency (1st and 15th)
# business month start frequency
# custom business month start frequency
# quarter end frequency
# business quarter endfrequency
# quarter start frequency
# business quarter start frequency
# year end frequency
# business year end frequency
# year start frequency
# business year start frequency
# business hour frequency
# hourly frequency
# minutely frequency
# secondly frequency
# milliseconds
# microseconds
# nanoseconds

# Our index
print(df.index)

# You need to call resample with the rule parameter, then you need to call some sort of aggregation function. This is because due to resampling, we need some sort of mathematical rule to join the rows by (mean,sum,count,etc...)
# Yearly Means
print(df.resample(rule='A').mean())

# ### Custom Resampling
# 
# You could technically also create your own custom resampling function:
def first_day(entry):
    """
    Returns the first instance of the period, regardless of samplling rate.
    """
    return entry[0]

print(df.resample(rule='A').apply(first_day))

df['Close'].resample('A').mean().plot(kind='bar')
plt.title('Yearly Mean Close Price for Walmart')
plt.savefig(PATH + 'year_mean_close.png', dpi=300)
plt.close()

df['Open'].resample('M').max().plot(kind='bar',figsize=(16,6))
plt.title('Monthly Max Opening Price for Walmart')
plt.savefig(PATH + 'month_max_open.png', dpi=300)
plt.close()
