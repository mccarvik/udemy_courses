#!/usr/bin/env python
# coding: utf-8

# # Quandl
# More info:
# https://www.quandl.com/tools/python
import pdb
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/7_data_sources/figs/'
import quandl
quandl.ApiConfig.api_key = 'J4d6zKiPjebay-zW7T8X'
# API_KEY = 'J4d6zKiPjebay-zW7T8X'

# ### Make a Basic Data Call
# This call gets the WTI Crude Oil price from the US Department of Energy:
mydata = quandl.get("EIA/PET_RWTC_D")
print(mydata.head())
mydata.plot(figsize=(12,6))
plt.savefig(PATH + 'quandl_1.png', dpi=300)
plt.close()
# Note that you need to know the "Quandl code" of each dataset you download. 
# In the above example, it is "EIA/PET_RWTC_D".

# ### Change Formats
# You can get the same data in a NumPy array:
mydata = quandl.get("EIA/PET_RWTC_D", returns="numpy")
print(mydata[:5])

# ### Specifying Data
# To set start and end dates:
mydata = quandl.get("FRED/GDP", start_date="2001-12-31", end_date="2005-12-31")
print(mydata.head())
mydata = quandl.get(["NSE/OIL.1", "WIKI/AAPL.4"])
print(mydata.head())

# ### Usage Limits
# The Quandl Python module is free. If you would like to make more than 
# 50 calls a day, however, you will need to create a free Quandl account and 
# set your API key:

# EXAMPLE
mydata = quandl.get("FRED/GDP")

# ## Database Codes
# 
# Each database on Quandl has a short (3-to-6 character) database ID.  For example:
# 
# * CFTC Commitment of Traders Data: CFTC
# * Core US Stock Fundamentals: SF1
# * Federal Reserve Economic Data: FRED
# 
# Each database contains many datasets.  Datasets have their own IDs which 
# are appended to their parent database ID, like this:
# 
# * Commitment of traders for wheat:  CFTC/W_F_ALL
# * Market capitalization for Apple:  SF1/AAPL_MARKETCAP
# * US civilian unemployment rate:  FRED/UNRATE
# 
# You can download all dataset codes in a database in a single API call, by 
# appending  /codes to your database request.  The call will return a ZIP 
# file containing a CSV.
# 
# ### Databases
# 
# 
# Every Quandl code has 2 parts: the database code (“WIKI”) which specifies 
# where the data comes from, and the dataset code (“FB”) which identifies 
# the specific time series you want.
# 
# You can find Quandl codes on their website, using their data browser.
# 
# https://www.quandl.com/search

# FOR STOCKS
mydata = quandl.get('WIKI/FB',start_date='2015-01-01',end_date='2017-01-01')
print(mydata.head())

mydata = quandl.get('WIKI/FB.1',start_date='2015-01-01',end_date='2017-01-01')
print(mydata.head())

mydata = quandl.get('WIKI/FB.7',start_date='2015-01-01',end_date='2017-01-01')
print(mydata.head())


# ### Housing Price Example
# 
# **Zillow Home Value Index (Metro): Zillow Rental Index - All Homes - San Francisco, CA**
# 
# The Zillow Home Value Index is Zillow's estimate of the median market value of zillow rental index - all homes within the metro of San Francisco, CA. This data is calculated by Zillow Real Estate Research (www.zillow.com/research) using their database of 110 million homes.
houses = quandl.get('ZILLOW/M11_ZRIAH')
print(houses.head())

houses.plot()
plt.savefig(PATH + 'housing.png', dpi=300)
plt.close()
