#!/usr/bin/env python
# coding: utf-8

# # Pandas Datareader
# 
# # READ THIS FIRST:
# 
# 
# ### THE STOCK APIS ARE OFTEN CHANGING DUE TO COMPANIES SUCH AS GOOGLE AND YAHOO CHANGING THEIR API ASPECT DUE TO A VARIETY OF FACTORS. CHECK THE PANDAS DATAREADER WEBSITE TO GET INFORMATION ON THE LATEST APIS, SINCE THIS WILL HAVE THE LATEST INFORMATION
# 
# ## https://pandas-datareader.readthedocs.io/en/latest/
# 
# ----
# ** NOTE: Not every geographical location works well with pandas datareader, your firewall may also block it!**
# 
# ---
# 
# Functions from pandas_datareader.data and pandas_datareader.wb extract data from various Internet sources into a pandas DataFrame. Currently the following sources are supported:
# 
# * Yahoo! Finance
# * Google Finance
# * Enigma
# * St.Louis FED (FRED)
# * Kenneth French’s data library
# * World Bank
# * OECD
# * Eurostat
# * Thrift Savings Plan
# * Oanda currency historical rate
# * Nasdaq Trader symbol definitions (remote_data.nasdaq_symbols)
# 
# It should be noted, that various sources support different kinds of data, so not all sources implement the same methods and the data elements returned might also differ.
import sys
import pandas_datareader.data as web
import datetime
start = datetime.datetime(2015, 1, 1)
end = datetime.datetime(2017, 1, 1)
# try 'yahoo' if Google doesn't work. make sure to check the website mentioned above
# search QA forums if you have any issues on this, many questions have already been answered there!
# yahoo google morningstar and iex all dont work
# facebook = web.DataReader("FB", 'iex', start, end)
# print(facebook.head())

# ### Experimental Options
# 
# # NOTE: Google has currently disable this. Check out pandas-datareader online docs for the latest information.
# 
# The Options class allows the download of options data from Google Finance.
# 
# The get_options_data method downloads options data for specified expiry date and provides a formatted DataFrame with a hierarchical index, so its easy to get to the specific option you want.
# 
# Available expiry dates can be accessed from the expiry_dates property.

from pandas_datareader.data import Options
# fb_options = Options('FB', 'yahoo')
# everything deprecated as well
# data = fb_options.get_options_data(expiry=fb_options.expiry_dates[0])
# print(data.head())


# # FRED
import pandas_datareader.data as web
import datetime
start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2017, 1, 1)
gdp = web.DataReader("GDP", "fred", start, end)
print(gdp.head())
