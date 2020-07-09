#!/usr/bin/env python
# coding: utf-8

# # Pipeline
# 
# This notebook is from the official Quantopian Guide on Pipelines. Make sure to
# visit their documentation for many more great resources!
# 
# Many trading algorithms have the following structure:
# 
# 1. For each asset in a known (large) set, compute N scalar values for the 
# asset based on a trailing window of data.
# 2. Select a smaller tradeable set of assets based on the values computed in (1).
# 3. Calculate desired portfolio weights on the set of assets selected in (2).
# 4. Place orders to move the algorithm’s current portfolio allocations to the
# desired weights computed in (3).
# 
# There are several technical challenges with doing this robustly. These include:
# 
# * efficiently querying large sets of assets
# * performing computations on large sets of assets
# * handling adjustments (splits and dividends)
# * asset delistings
# 
# Pipeline exists to solve these challenges by providing a uniform API for
# expressing computations on a diverse collection of datasets.

# ## Factors
# A factor is a function from an asset and a moment in time to a numerical value.
# 
# A simple example of a factor is the most recent price of a security. Given a
# security and a specific point in time, the most recent price is a number.
# Another example is the 10-day average trading volume of a security. 
# Factors are most commonly used to assign values to securities which can
# then be used in a number of ways. A factor can be used in each of the following procedures:
# * computing target weights
# * generating alpha signal
# * constructing other, more complex factors
# * constructing filters

# ## Filters
# A filter is a function from an asset and a moment in time to a boolean.
# An example of a filter is a function indicating whether a security's price is
# below $10. Given a security and a point in time, this evaluates to either 
# True or False. Filters are most commonly used for describing sets of assets 
# to include or exclude for some particular purpose.

# ## Classifiers
# A classifier is a function from an asset and a moment in time to a categorical output.
# More specifically, a classifier produces a string or an int that doesn't 
# represent a numerical value (e.g. an integer label such as a sector code). 
# Classifiers are most commonly used for grouping assets for complex 
# transformations on Factor outputs. An example of a classifier is the exchange 
# on which an asset is currently being traded.
import sys, pdb
from quantopian.pipeline import Pipeline


def make_pipeline():
    return Pipeline()

pipe = make_pipeline()

from quantopian.research import run_pipeline
result = run_pipeline(pipe,'2017-01-01','2017-01-01')

print(result.head(10))
print(result.info())

# # Data
from quantopian.pipeline.data.builtin import USEquityPricing

# ## Factors
# 
# Remember, Factors take in an asset and a timestamp and return some numerical value.
from quantopian.pipeline.factors import BollingerBands,SimpleMovingAverage,EWMA

SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)

def make_pipeline2():
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    return Pipeline(columns={
        '30 Day Mean Close':mean_close_30
    })

results = run_pipeline(make_pipeline2(),'2017-01-01','2017-01-01')
print(results.head(20))

def make_pipeline3():
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    latest_close = USEquityPricing.close.latest
    
    return Pipeline(columns={
        '30 Day Mean Close':mean_close_30,
        'Latest Close':latest_close
    })

results = run_pipeline(make_pipeline3(),'2017-01-01','2017-01-01')
print(results.head(10))

# ## Combining Factors

def make_pipeline4():
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    return Pipeline(columns={
        'Percent Difference':percent_difference,
        '30 Day Mean Close':mean_close_30,
        'Latest Close':latest_close
    })

results = run_pipeline(make_pipeline4(),'2017-01-01','2017-01-01')
print(results.head())

# # Filters and Screens
# 
# Filters take in an asset and a timestamp and return a boolean
last_close_price = USEquityPricing.close.latest
close_price_filter = last_close_price > 20
print(close_price_filter)

def make_pipeline5():
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    perc_diff_check = percent_difference > 0 
    
    return Pipeline(columns={
        'Percent Difference':percent_difference,
        '30 Day Mean Close':mean_close_30,
        'Latest Close':latest_close,
        'Positive Percent Diff': perc_diff_check
    })

results = run_pipeline(make_pipeline5(),'2017-01-01','2017-01-01')
print(results.head())


# ## Screens
def make_pipeline6():
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    perc_diff_check = percent_difference > 0 
    
    return Pipeline(columns={
                            'Percent Difference':percent_difference,
                            '30 Day Mean Close':mean_close_30,
                            'Latest Close':latest_close,
                            'Positive Percent Diff': perc_diff_check},
                    screen=perc_diff_check)

results = run_pipeline(make_pipeline6(),'2017-01-01','2017-01-01')
print(results.head())

# ### Reverse a screen
def make_pipeline7():
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    perc_diff_check = percent_difference > 0 
    
    return Pipeline(columns={
                            'Percent Difference':percent_difference,
                            '30 Day Mean Close':mean_close_30,
                            'Latest Close':latest_close,
                            'Positive Percent Diff': perc_diff_check},
                    screen=~perc_diff_check)

results = run_pipeline(make_pipeline7(),'2017-01-01','2017-01-01')
print(results.head())

# ## Combine Filters
def make_pipeline8():
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    perc_diff_check = percent_difference > 0 
    small_price = latest_close < 5
    
    final_filter = perc_diff_check & small_price
    
    return Pipeline(columns={
                            'Percent Difference':percent_difference,
                            '30 Day Mean Close':mean_close_30,
                            'Latest Close':latest_close,
                            'Positive Percent Diff': perc_diff_check},
                    screen=final_filter)

results = run_pipeline(make_pipeline8(),'2017-01-01','2017-01-01')
print(results.head())


# # Masking
# 
# Sometimes we want to ignore certain assets when computing pipeline expresssions. 
# There are two common cases where ignoring assets is useful:
# * We want to compute an expression that's computationally expensive, and we 
# know we only care about results for certain assets.
# * We want to compute an expression that performs comparisons between assets, 
# but we only want those comparisons to be performed against a subset of all assets. 

def make_pipeline9():
    # Create Filters for Masks First
    latest_close = USEquityPricing.close.latest
    small_price = latest_close < 5
    
    # Pass in the mask
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10,mask=small_price)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30,mask=small_price)
    
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    perc_diff_check = percent_difference > 0 
    
    
    final_filter = perc_diff_check
    
    return Pipeline(columns={
                            'Percent Difference':percent_difference,
                            '30 Day Mean Close':mean_close_30,
                            'Latest Close':latest_close,
                            'Positive Percent Diff': perc_diff_check},
                    screen=final_filter)

results = run_pipeline(make_pipeline9(),'2017-01-01','2017-01-01')
print(results.head())
print(len(results))

# # Classifiers
# 
# A classifier is a function from an asset and a moment in time to a categorical
# output such as a string or integer label.
from quantopian.pipeline.data import morningstar
from quantopian.pipeline.classifiers.morningstar import Sector

morningstar_sector = Sector()
exchange = morningstar.share_class_reference.exchange_id.latest
print(exchange)

# ### Classifier Methods
# 
# * eq (equals)
# * isnull
# * startswith
nyse_filter = exchange.eq('NYS')

def make_pipeline10():
    # Create Filters for Masks First
    latest_close = USEquityPricing.close.latest
    small_price = latest_close < 5
    
    # Classifier
    nyse_filter = exchange.eq('NYS')
    
    # Pass in the mask
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10,mask=small_price)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30,mask=small_price)
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    perc_diff_check = percent_difference > 0 
    
    
    final_filter = perc_diff_check & nyse_filter
    
    return Pipeline(columns={
                            'Percent Difference':percent_difference,
                            '30 Day Mean Close':mean_close_30,
                            'Latest Close':latest_close,
                            'Positive Percent Diff': perc_diff_check},
                    screen=final_filter)
results = run_pipeline(make_pipeline10(),'2017-01-01','2017-01-01')
print(results.head())
print(len(results))

# # Pipelines in Quantopian IDE
from quantopian.pipeline import Pipeline
from quantopian.algorithm import attach_pipeline, pipeline_output

def initialize(context):
    my_pipe = make_pipeline()
    attach_pipeline(my_pipe, 'my_pipeline')

def make_pipeline11():
    return Pipeline()

def before_trading_start(context, data):
    # Store our pipeline output DataFrame in context.
    context.output = pipeline_output('my_pipeline')
