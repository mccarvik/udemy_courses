#!/usr/bin/env python
# coding: utf-8

# # Pipeline
# 
# This notebook is from the official Quantopian Guide on Pipelines. Make sure to visit their documentation for many more great resources!
# 
# Many trading algorithms have the following structure:
# 
# 1. For each asset in a known (large) set, compute N scalar values for the asset based on a trailing window of data.
# 2. Select a smaller tradeable set of assets based on the values computed in (1).
# 3. Calculate desired portfolio weights on the set of assets selected in (2).
# 4. Place orders to move the algorithm’s current portfolio allocations to the desired weights computed in (3).
# 
# There are several technical challenges with doing this robustly. These include:
# 
# * efficiently querying large sets of assets
# * performing computations on large sets of assets
# * handling adjustments (splits and dividends)
# * asset delistings
# 
# Pipeline exists to solve these challenges by providing a uniform API for expressing computations on a diverse collection of datasets.

# ## Factors
# A factor is a function from an asset and a moment in time to a numerical value.
# 
# A simple example of a factor is the most recent price of a security. Given a security and a specific point in time, the most recent price is a number. Another example is the 10-day average trading volume of a security. Factors are most commonly used to assign values to securities which can then be used in a number of ways. A factor can be used in each of the following procedures:
# * computing target weights
# * generating alpha signal
# * constructing other, more complex factors
# * constructing filters

# ## Filters
# A filter is a function from an asset and a moment in time to a boolean.
# An example of a filter is a function indicating whether a security's price is below $10. Given a security and a point in time, this evaluates to either True or False. Filters are most commonly used for describing sets of assets to include or exclude for some particular purpose.

# ## Classifiers
# A classifier is a function from an asset and a moment in time to a categorical output.
# More specifically, a classifier produces a string or an int that doesn't represent a numerical value (e.g. an integer label such as a sector code). Classifiers are most commonly used for grouping assets for complex transformations on Factor outputs. An example of a classifier is the exchange on which an asset is currently being traded.

# In[1]:


from quantopian.pipeline import Pipeline


# In[22]:


def make_pipeline():
    return Pipeline()


# In[23]:


pipe = make_pipeline()


# In[24]:


from quantopian.research import run_pipeline


# In[25]:


result = run_pipeline(pipe,'2017-01-01','2017-01-01')


# In[26]:


result.head(10)


# In[27]:


result.info()


# # Data

# In[36]:


from quantopian.pipeline.data.builtin import USEquityPricing


# ## Factors
# 
# Remember, Factors take in an asset and a timestamp and return some numerical value.

# In[38]:


from quantopian.pipeline.factors import BollingerBands,SimpleMovingAverage,EWMA


# In[40]:


SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)


# In[41]:


def make_pipeline():
    
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    
    return Pipeline(columns={
        '30 Day Mean Close':mean_close_30
    })


# In[46]:


results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')


# In[48]:


results.head(20)


# In[49]:


def make_pipeline():
    
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    latest_close = USEquityPricing.close.latest
    
    return Pipeline(columns={
        '30 Day Mean Close':mean_close_30,
        'Latest Close':latest_close
    })


# In[50]:


results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')


# In[52]:


results.head(10)


# ## Combining Factors

# In[54]:


def make_pipeline():
    
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10-mean_close_30) / mean_close_30
    
    return Pipeline(columns={
        'Percent Difference':percent_difference,
        '30 Day Mean Close':mean_close_30,
        'Latest Close':latest_close
    })


# In[55]:


results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')


# In[56]:


results.head()


# # Filters and Screens
# 
# Filters take in an asset and a timestamp and return a boolean

# In[57]:


last_close_price = USEquityPricing.close.latest
close_price_filter = last_close_price > 20


# In[58]:


close_price_filter


# In[59]:


def make_pipeline():
    
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


# In[60]:


results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head()


# ## Screens

# In[61]:


def make_pipeline():
    
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


# In[62]:


results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head()


# ### Reverse a screen

# In[63]:


def make_pipeline():
    
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


# In[64]:


results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head()


# ## Combine Filters

# In[65]:


def make_pipeline():
    
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


# In[66]:


results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head()


# # Masking
# 
# Sometimes we want to ignore certain assets when computing pipeline expresssions. There are two common cases where ignoring assets is useful:
# * We want to compute an expression that's computationally expensive, and we know we only care about results for certain assets.
# * We want to compute an expression that performs comparisons between assets, but we only want those comparisons to be performed against a subset of all assets. 

# In[83]:


def make_pipeline():
    
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


# In[84]:


results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head()


# In[85]:


len(results)


# # Classifiers
# 
# A classifier is a function from an asset and a moment in time to a categorical output such as a string or integer label.

# In[74]:


from quantopian.pipeline.data import morningstar
from quantopian.pipeline.classifiers.morningstar import Sector


# In[75]:


morningstar_sector = Sector()


# In[76]:


exchange = morningstar.share_class_reference.exchange_id.latest


# In[77]:


exchange


# ### Classifier Methods
# 
# * eq (equals)
# * isnull
# * startswith

# In[79]:


nyse_filter = exchange.eq('NYS')


# In[80]:


def make_pipeline():
    
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


# In[81]:


results = run_pipeline(make_pipeline(),'2017-01-01','2017-01-01')
results.head()


# In[82]:


len(results)


# # Pipelines in Quantopian IDE

# In[ ]:


from quantopian.pipeline import Pipeline
from quantopian.algorithm import attach_pipeline, pipeline_output

def initialize(context):
    my_pipe = make_pipeline()
    attach_pipeline(my_pipe, 'my_pipeline')

def make_pipeline():
    return Pipeline()

def before_trading_start(context, data):
    # Store our pipeline output DataFrame in context.
    context.output = pipeline_output('my_pipeline')


# In[ ]:




