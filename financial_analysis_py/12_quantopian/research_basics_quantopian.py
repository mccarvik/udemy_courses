#!/usr/bin/env python
# coding: utf-8

# # 01-Quantopian Research Basics
# 
# **Please remember that this notebook will only work on Quantopian! Make an account 
# and upload this notebook file. These commands and functions won't work except on 
# the Quantopian trading platform!**
# 
# Note a lot of the written markdown text in this notebook comes direclty from the 
# Quantopian docs and tutorials, definitely check those out as well, they're great!
# 
# ## Research
# 
# The notebook format allows us to easily gather information about variuos securities 
# all within the Quantopian platform. Keep in mind this is different than the base 
# coding platform of quantopian, which focuses on actually implementing and
# backtesting trading strategies.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/11_py_fin_fundamentals/figs/'
# ## Getting Information
# 
# Let's go over a few key functions:
# 
# * get_pricing()
# * symbols()
# * local_csv()
# * get_backtest()
# * get_fundamentals()

# ## get_pricing()
# 
# The `get_pricing` function provides access to 12 years of US Equity pricing data:
# the same data used by the Quantopian backtester.
# 
# `get_pricing` returns a <b>pandas object</b>. This could be a panel, dataframe or 
# series depending on the input values. 
mcdon = get_pricing('MCD',
                    start_date='2017-01-01', 
                    end_date = '2017-02-01', 
                    frequency='minute')
print(mcdon.head())
print(mcdon.info())

# Can only go about 12 years back
# which is really all you need for algo trading, 
# going back further probably is more noise than signal.
mcdon = get_pricing('MCD',
                    start_date='2005-01-01', 
                    end_date = '2017-01-01', 
                    frequency='daily')


mcdon['close_price'].plot()
plt.savefig(PATH + 'mcd_price.png', dpi=300)
plt.close()

mcdon['close_price'].pct_change(1).hist(bins=100,figsize=(6,4))
plt.savefig(PATH + 'mcd_hist.png', dpi=300)
plt.close()

# ## symbols()
# 
# By default `symbols` returns the security object for a ticker symbol. Specify a 
# ticker symbol, or list of symbols, as a string and get a list of security objects back. 
# 
# - Use `symbol_reference_date` to identify which date you want the symbol back for 
# a particular ticker symbol. 
# - Specify how you would like missing results to be handled with `handle_missing`
# 
# 
mcdon_eq_info = symbols('MCD')
print(type(mcdon_eq_info))

for key in mcdon_eq_info.to_dict():
    print(key)
    print(mcdon_eq_info.to_dict()[key])
    print('\n')

# NOTE!!!!!!!!!!!!!!!!!!!!!!!!!!!! - fundamentals not used like this anymore
# need to go thru pipelines as shown in a future lecture
# ## get_fundamentals()
# 
# The `get_fundamentals` function provides programmatic access to the Quantopian 
# fundamental database. Based on data provided by Morningstar, `get_fundamentals` 
# provides over 600 corporate metrics dating back to 2002 (to match Quantopian's 
# pricing data). 
# 
# The data used by this research function is the same data used by the 
# `get_fundamentals` function used in the Quantopian IDE. The fields are described 
# in the Quantopian help documents: http://www.quantopian.com/help/fundamentals.
# 
# Have to do this first in the notebook:
fundamentals = init_fundamentals()

# The get_fundamentals() function takes in a SQLAlchemy query which can be quite 
# complicated and strange looking at first. Basically it allows you to filter by a 
# variety of fundamentals (things like Market Cap, P/E Ratio, or even city of HQ). 
# Check out the link above for all the things you can filter by!
# 
# Let's walk through a few query examples.
# 
# First call fundamentals and use tab to check out the various options:
# fundamentals. # call tab here as in the video!
# Market Cap
my_query = query(fundamentals.valuation.market_cap)
my_funds = get_fundamentals(my_query,'2017-01-01')
print(my_funds.info())
# Basically just returns the market cap of everything
# for 2017-01-01
print(my_funds.head())
# What you usualy do is filter by other qualities after the query!

# Only get companies worth 500 billion or more (that's a lot of dough!)
big_companies = (query(fundamentals.valuation.market_cap).
                 filter(fundamentals.valuation.market_cap > 500000000000) )
my_big_funds = get_fundamentals(big_companies,'2017-07-19')
print(my_big_funds)
print(7.82 * 10**11)
print(get_fundamentals())
