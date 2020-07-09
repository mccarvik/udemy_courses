#!/usr/bin/env python
# coding: utf-8

# # Pipeline Example
from quantopian.pipeline import Pipeline
from quantopian.research import run_pipeline
from quantopian.pipeline.data.builtin import USEquityPricing

# ## Getting the Securities we want.
# 
# ### The Q500US and Q1500US
# 
# These gropus of tradeable stocks are refered to as "universes", because all 
# your trades will use these stocks as their "Universe" of available stock, they 
# won't be trading with anything outside these groups.
from quantopian.pipeline.filters import Q1500US

# There are two main benefits of the Q500US and Q1500US. Firstly, they greatly 
# reduce the risk of an order not being filled. Secondly, they allow for more 
# meaningful comparisons between strategies as now they will be used as the 
# standard universes for algorithms.
universe = Q1500US()

# ## Filtering the universe further with Classifiers
# 
# Let's only grab stocks in the energy sector: https://www.quantopian.com/help/fundamentals#industry-sector
from quantopian.pipeline.data import morningstar
sector = morningstar.asset_classification.morningstar_sector_code.latest

# Alternative:
#from quantopian.pipeline.classifiers.morningstar import Sector
#morningstar_sector = Sector()
energy_sector = sector.eq(309)

# ## Masking Filters
# 
# Masks can be also be applied to methods that return filters like top, bottom, and percentile_between.
# 
# Masks are most useful when we want to apply a filter in the earlier steps of a 
# combined computation. For example, suppose we want to get the 50 securities with 
# the highest open price that are also in the top 10% of dollar volume. 
# 
# Suppose that we then want the 90th-100th percentile of these securities by 
# close price. We can do this with the following:
from quantopian.pipeline.factors import SimpleMovingAverage, AverageDollarVolume

# Dollar volume factor
dollar_volume = AverageDollarVolume(window_length=30)

# High dollar volume filter
high_dollar_volume = dollar_volume.percentile_between(90,100)

# Top open price filter (high dollar volume securities)
top_open_price = USEquityPricing.open.latest.top(50, mask=high_dollar_volume)

# Top percentile close price filter (high dollar volume, top 50 open price)
high_close_price = USEquityPricing.close.latest.percentile_between(90, 100, mask=top_open_price)

# ## Applying Filters and Factors
# 
# Let's apply our own filters, following along with some of the examples above. 
# Let's select the following securities:
# 
# * Stocks in Q1500US
# * Stocks that are in the energy Sector
# * They must be relatively highly traded stocks in the market (by dollar volume traded, 
# need to be in the top 5% traded)
# 
# Then we'll calculate the percent difference as we've done previously. Using 
# this percent difference we'll create an unsophisticated strategy that shorts 
# anything with negative percent difference (the difference between the 10 day 
# mean and the 30 day mean).

def make_pipeline():
    
    # Base universe filter.
    base_universe = Q1500US()
    
    # Sector Classifier as Filter
    energy_sector = sector.eq(309)
    
    # Masking Base Energy Stocks
    base_energy = base_universe & energy_sector
    
    # Dollar volume factor
    dollar_volume = AverageDollarVolume(window_length=30)

    # Top half of dollar volume filter
    high_dollar_volume = dollar_volume.percentile_between(95,100)
    
    # Final Filter Mask
    top_half_base_energy = base_energy & high_dollar_volume
    
    # 10-day close price average.
    mean_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10, mask=top_half_base_energy)

    # 30-day close price average.
    mean_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30, mask=top_half_base_energy)

    # Percent difference factor.
    percent_difference = (mean_10 - mean_30) / mean_30
    
    # Create a filter to select securities to short.
    shorts = percent_difference < 0
    
    # Create a filter to select securities to long.
    longs = percent_difference > 0
    
    # Filter for the securities that we want to trade.
    securities_to_trade = (shorts | longs)
    
    return Pipeline(
        columns={
            'longs': longs,
            'shorts': shorts,
            'percent_diff':percent_difference
        },
        screen=securities_to_trade
    )

result = run_pipeline(make_pipeline(), '2015-05-05', '2015-05-05')
print(result)
print(result.info())



# # Executing this Strategy in the IDE
from quantopian.algorithm import attach_pipeline,pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import AverageDollarVolume,SimpleMovingAverage
from quantopian.pipeline.filters.morningstar import Q1500US
from quantopian.pipeline.data import morningstar

def initialize(context):
    schedule_function(my_rebalance,date_rules.week_start(),time_rules.market_open(hours=1))
    
    my_pipe = make_pipeline()
    attach_pipeline(my_pipe,'my_pipeline')
    
    
def my_rebalance(context,data):
    for security in context.portfolio.positions:
        if security not in context.longs and security not in context.shorts and data.can_trade(security):
            order_target_percent(security,0)
            
    for security in context.longs:
        if data.can_trade(security):
            order_target_percent(security,context.long_weight)

    for security in context.shorts:
        if data.can_trade(security):
            order_target_percent(security,context.short_weight)


def my_compute_weights(context):
    
    if len(context.longs)==0:
        long_weight = 0
    else:
        long_weight = 0.5 / len(context.longs)
  
    if len(context.shorts)==0:
        short_weight = 0
    else:
        short_weight = 0.5 / len(context.shorts)
    
    return (long_weight,short_weight)


def before_trading_start(context,data):
    context.output = pipeline_output('my_pipeline')
    
    # LONG
    context.longs = context.output[context.output['longs']].index.tolist()
    
    # SHORT
    context.shorts = context.output[context.output['shorts']].index.tolist()


    context.long_weight,context.short_weight = my_compute_weights(context)


def make_pipeline2():
    
    # Universe Q1500US
    base_universe = Q1500US()
    
    # Energy Sector
    sector = morningstar.asset_classification.morningstar_sector_code.latest
    energy_sector = sector.eq(309)
    
    # Make Mask of 1500US and Energy
    base_energy = base_universe & energy_sector
    
    # Dollar Volume (30 Days) Grab the Info
    dollar_volume = AverageDollarVolume(window_length=30)
    
    # Grab the top 5% in avg dollar volume
    high_dollar_volume = dollar_volume.percentile_between(95,100)
     
    # Combine the filters
    top_five_base_energy = base_energy & high_dollar_volume
    
    # 10 day mean close
    mean_10 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=10,mask=top_five_base_energy)
    
    # 30 day mean close
    mean_30 = SimpleMovingAverage(inputs=[USEquityPricing.close],window_length=30,mask=top_five_base_energy)
    
    # Percent Difference
    percent_difference = (mean_10-mean_30)/mean_30
    
    # List of Shorts
    shorts = percent_difference < 0
    
    # List of Longs
    longs = percent_difference > 0
    
    # Final Mask/Filter for anything in shorts or longs
    securities_to_trade = (shorts | longs)
    
    # Return Pipeline
    return Pipeline(columns={
        'longs':longs,
        'shorts':shorts,
        'perc_diff':percent_difference
    },screen=securities_to_trade)

