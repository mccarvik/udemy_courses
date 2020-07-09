#!/usr/bin/env python
# coding: utf-8

# # Basic Algorithm Methods
# 
# Let's algorithmically test our earlier optimized tech portfolio strategy with Quantopian!
# 
# #### THIS CODE ONLY WORKS ON QUANTOPIAN. EACH CELL CORRESPONDS WITH A PART OF THE VIDEO 
# LECTURE. MAKE SURE TO WATCH THE VIDEOS FOR CLARITY ON THIS!

# **initialize()**
# 
# initialize() is called exactly once when our algorithm starts and requires context as input.
# 
# context is an augmented Python dictionary used for maintaining state during our 
# backtest or live trading, and can be referenced in different parts of our algorithm. 
# context should be used instead of global variables in the algorithm. Properties can be 
# accessed using dot notation (context.some_property).

# ** handle_data() **
# 
# handle_data() is called once at the end of each minute and requires context and data as 
# input. context is a reference to the same dictionary in initialize() and data is an 
# object that stores several API functions.

# ## Our Tech Stock Optimized Portfolio
# 
# Let's use the tech stock portfolio we calculated earlier. Keep in mind that handle_data() 
# is readjusting our portfolio every minute! That may be unreasonable for certain algorithms,
# but for this example, we will just continue with these basics functions.

def initialize(context):
    # Reference to Tech Stocks
    context.aapl = sid(24)
    context.csco = sid(1900)
    context.amzn = sid(16841)

def handle_data(context, data):
    # Position our portfolio optimization!
    order_target_percent(context.aapl, .27)
    order_target_percent(context.csco, .20)
    order_target_percent(context.amzn, .53)


# ### Grabbing Current Data
# ### data.current()
# data.current() can be used to retrieve the most recent value of a given field(s) for a 
# given asset(s). data.current() requires two arguments: the asset or list of assets, and 
# the field or list of fields being queried. Possible fields include 'price', 'open', 'high',
# 'low', 'close', and 'volume'. The output type will depend on the input types

def initialize(context):
    # Reference to Tech Stocks
    context.techies = [sid(16841),sid(24),sid(1900)]

def handle_data(context, data):
    # Position our portfolio optimization!
    tech_close = data.current(context.techies,'close')
    print(type(tech_close)) # Pandas Series
    print(tech_close) # Closing Prices 


# ##### Note! You can use data.is_stale(sid(#)) to check if the results of data.current() 
# where generated at the current bar (the timeframe) or were forward filled from a previous time.

# ### Checking for trading
# ### data.can_trade()
# 
# data.can_trade() is used to determine if an asset(s) is currently listed on a 
# supported exchange and can be ordered. If data.can_trade() returns True for a 
# particular asset in a given minute bar, we are able to place an order for that
# asset in that minute. This is an important guard to have in our algorithm if 
# we hand-pick the securities that we want to trade. It requires a single 
# argument: an asset or a list of assets.
def initialize(context):
    # Reference to amazn
    context.amzn = sid(16841)
    
def handle_data(context, data):
    # This insures we don't hit an exception!
    if data.can_trade(sid(16841)):
        order_target_percent(context.amzn, 1.0)

# # Checking Historical Data
# 
# When your algorithm calls data.history on equities, the returned data is adjusted for
# splits, mergers, and dividends as of the current simulation date. In other words, when your
# algorithm asks for a historical window of prices, and there is a split in the middle of 
# that window, the first part of that window will be adjusted for the split. This adustment 
# is done so that your algorithm can do meaningful calculations using the values in the window.
# 
# This code queries the last 20 days of price history for a static set of securities.
# Specifically, this returns the closing daily price for the last 20 days,
# including the current price for the current day. Equity prices are split- 
# and dividend-adjusted as of the current date in the simulation:

def initialize(context):
    # AAPL, MSFT, and SPY
    context.assets = [sid(24), sid(1900), sid(16841)]

def before_trading_start(context,data):
    price_history = data.history(context.assets,fields="price", bar_count=5, frequency="1d")
    print(price_history)


# The bar_count field specifies the number of days or minutes to include in the
# pandas DataFrame returned by the history function. This parameter accepts only 
# integer values.
# 
# The frequency field specifies how often the data is sampled: daily or minutely.
# Acceptable inputs are ‘1d’ or ‘1m’. For other frequencies, use the pandas 
# resample function.

# ### Examples
# Below are examples of code along with explanations of the data returned.
# 
# ### Daily History
# 
# Use "1d" for the frequency. The dataframe returned is always in daily bars. 
# The bars never span more than one trading day. For US equities, a daily bar
# captures the trade activity during market hours (usually 9:30am-4:00pm ET).
# For US futures, a daily bar captures the trade activity from 6pm-6pm ET
# (24 hours). For example, the Monday daily bar captures trade activity from 
# 6pm the day before (Sunday) to 6pm on the Monday. Tuesday's daily bar will 
# run from 6pm Monday to 6pm Tuesday, etc. For either asset class, the last
# bar, if partial, is built using the minutes of the current day.
# 
# ### Examples (assuming context.assets exists):
# 
# * data.history(context.assets, "price", 1, "1d") returns the current price.
# * data.history(context.assets, "volume", 1, "1d") returns the volume since the current day's open, even if it is partial.
# * data.history(context.assets, "price", 2, "1d") returns yesterday's close price and the current price.
# * data.history(context.assets, "price", 6, "1d") returns the prices for the previous 5 days and the current price.
# 
# 
# ### Minute History
# 
# Use "1m" for the frequency.
# 
# Examples (assuming context.assets exists):
# 
# * data.history(context.assets, "price", 1, "1m") returns the current price.
# * data.history(context.assets, "price", 2, "1m") returns the previous minute's close price and the current price.
# * data.history(context.assets, "volume", 60, "1m") returns the volume for the previous 60 minutes.

# # Scheduling
# 
# Use schedule_function to indicate when you want other functions to occur. 
# The functions passed in must take context and data as parameters.

def initialize(context):
    context.appl = sid(49051)

    # At ebginning of trading week
    # At Market Open, set 10% of portfolio to be apple
    schedule_function(open_positions, date_rules.week_start(), time_rules.market_open())
    
    # At end of trading week
    # 30 min before market close, dump all apple stock.
    schedule_function(close_positions, date_rules.week_end(), time_rules.market_close(minutes=30))

def open_positions(context, data):
    order_target_percent(context.appl, 0.10)

def close_positions(context, data):
    order_target_percent(context.appl, 0)


# # Portfolio Information
# 
# You can get portfolio information and record it!
def initialize(context):
    context.amzn = sid(16841)
    context.ibm = sid(3766)

    schedule_function(rebalance, date_rules.every_day(), time_rules.market_open())
    schedule_function(record_vars, date_rules.every_day(), time_rules.market_close())

def rebalance(context, data):
    # Half of our portfolio long on amazn
    order_target_percent(context.amzn, 0.50)
    # Half is shorting IBM
    order_target_percent(context.ibm, -0.50)

def record_vars(context, data):

    # Plot the counts
    record(amzn_close=data.current(context.amzn,'close'))
    record(ibm_close=data.current(context.ibm,'close'))


# # Slippage and Commision 
# 
# ### Slippage
# Slippage is where a simulation estimates the impact of orders on the fill 
# rate and execution price they receive. When an order is placed for a trade, 
# the market is affected. Buy orders drive prices up, and sell orders drive 
# prices down; this is generally referred to as the price_impact of a trade.
# Additionally, trade orders do not necessarily fill instantaneously. Fill 
# rates are dependent on the order size and current trading volume of the 
# ordered security. The volume_limit determines the fraction of a security's
# trading volume that can be used by your algorithm.
# 
# In backtesting and non-brokerage paper trading (Quantopian paper trading), a
# slippage model can be specified in initialize() using set_slippage().
# There are different builtin slippage models that can be used, as well as
# the option to set a custom model. By default (if a slippage model is not 
# specified), the following volume share slippage model is used:
set_slippage(slippage.VolumeShareSlippage(volume_limit=0.025, price_impact=0.1))


# Using the default model, if an order of 60 shares is placed for a given stock, 
# then 1000 shares of that stock trade in each of the next several minutes
# and the volume_limit is 0.025, then our trade order will be split into three 
# orders (25 shares, 25 shares, and 10 shares) that execute over the next 3 minutes.
# 
# At the end of each day, all open orders are canceled, so trading liquid 
# stocks is generally a good idea. Additionally, orders placed exactly at
# market close will not have time to fill, and will be canceled.

# ### Commision
# 
# To set the cost of trades, we can specify a commission model in initialize() 
# using set_commission(). By default (if a commission model is not specified), 
# the following commission model is used:
set_commission(commission.PerShare(cost=0.0075, min_trade_cost=1))


# The default commission model charges $0.0075 per share, with a minimum trade cost of $1.
# 
# Slippage and commission models can have an impact on the performance of a
# backtest. The default models used by Quantopian are fairly realistic, and 
# it is highly recommended that you use them.

# # Great Job!
# 
# Those are all the basics of Quantopians Tutorial! With these key functions 
# you actually know enough to begin trading! 
