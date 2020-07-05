#!/usr/bin/env python
# coding: utf-8
# ETS = Error - Trend - Seasonality
# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___
# <center>*Copyright Pierian Data 2017*</center>
# <center>*For more information, visit us at www.pieriandata.com*</center>
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/10_time_series_analysis/figs/'
airline = pd.read_csv('airline_passengers.csv',index_col="Month")
print(airline.head())

airline.plot()
plt.savefig(PATH + 'airline_ets.png', dpi=300)
plt.close()

# ## ETS
# 
# We can use an additive model when it seems that the trend is more linear and the seasonality and trend components seem to be constant over time (e.g. every year we add 10,000 passengers). A multiplicative model is more appropriate when we are increasing (or decreasing) at a non-linear rate (e.g. each year we double the amount of passengers).
# 
# Based off this chart, it looks like the trend in these earlier days is slightly increasing at a higher rate than just linear (although it is a  bit hard to tell from this one plot).
# Get data in correct format
airline.dropna(inplace=True)
airline.index = pd.to_datetime(airline.index)
print(airline.head())

from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(airline['Thousands of Passengers'], model='multiplicative')
result.plot()
plt.savefig(PATH + 'airline_ets_seasonal.png', dpi=300)
plt.close()

# You may accidentally see two of the same plots here, not to worry,
# just a small bug with statsmodels function.

