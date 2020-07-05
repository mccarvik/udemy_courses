#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___
# <center>*Copyright Pierian Data 2017*</center>
# <center>*For more information, visit us at www.pieriandata.com*</center>

# # Introduction to Statsmodels
# 
# Statsmodels is a Python module that provides classes and functions for the 
# estimation of many different statistical models, as well as for conducting 
# statistical tests, and statistical data exploration. An extensive list of 
# result statistics are available for each estimator. The results are tested 
# against existing statistical packages to ensure that they are correct. The 
# package is released under the open source Modified BSD (3-clause) license. The 
# online documentation is hosted at statsmodels.org.
# 
# The reason we will cover it for use in this course, is that you may find it 
# very useful later on when discussing time series data (typical of quantitative 
# financial analysis).
# 
# Let's walk through a very simple example of using statsmodels!
import pdb, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/10_time_series_analysis/figs/'
# get_ipython().run_line_magic('matplotlib', 'inline')
# You can safely ignore the warning:
#  Please use the pandas.tseries module instead. from pandas.core import datetools
import statsmodels.api as sm
df = sm.datasets.macrodata.load_pandas().data
print(sm.datasets.macrodata.NOTE)
print(df.head())
index = pd.Index(sm.tsa.datetools.dates_from_range('1959Q1', '2009Q3'))
df.index = index
print(df.head())

df['realgdp'].plot()
plt.ylabel("REAL GDP")
plt.savefig(PATH + 'real_gdp.png', dpi=300)
plt.close()

# ## Using Statsmodels to get the trend
# The Hodrick-Prescott filter separates a time-series  y_t  into a trend  τ_t and 
# a cyclical component  ζt
# 
# $y_t = \tau_t + \zeta_t$
# 
# The components are determined by minimizing the following quadratic loss 
# function
# 
# $\min_{\\{ \tau_{t}\\} }\sum_{t}^{T}\zeta_{t}^{2}+\lambda\sum_{t=1}^{T}\left[\left(\tau_{t}-\tau_{t-1}\right)-\left(\tau_{t-1}-\tau_{t-2}\right)\right]^{2}$

# Tuple unpacking
gdp_cycle, gdp_trend = sm.tsa.filters.hpfilter(df.realgdp)
print(gdp_cycle)
print(type(gdp_cycle))
df["trend"] = gdp_trend

df[['trend','realgdp']].plot()
plt.savefig(PATH + 'gdp_trend.png', dpi=300)
plt.close()

df[['trend','realgdp']]["2000-03-31":].plot(figsize=(12,8))
plt.savefig(PATH + 'trend_2000.png', dpi=300)
plt.close()

# ## Great job!
