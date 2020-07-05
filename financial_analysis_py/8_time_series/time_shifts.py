#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___
# <center>*Copyright Pierian Data 2017*</center>
# <center>*For more information, visit us at www.pieriandata.com*</center>

# # Time Shifting
# 
# Sometimes you may need to shift all your data up or down along the time series 
# index, in fact, a lot of pandas built-in methods do this under the hood. 
# This isn't something we won't do often in the course, but its definitely good 
# to know about this anyways!
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('time_data/walmart_stock.csv',index_col='Date')
df.index = pd.to_datetime(df.index)
print(df.head())
print(df.tail())

# ## .shift() forward
print(df.shift(1).head())

# You will lose that last piece of data that no longer has an index!
print(df.shift(1).tail())

# ## shift() backwards
print(df.shift(-1).head())
print(df.shift(-1).tail())

# ## Shifting based off Time String Code 
# ### Using tshift()

# Shift everything forward one month
print(df.tshift(periods=1,freq='M').head())
