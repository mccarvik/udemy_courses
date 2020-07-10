#!/usr/bin/env python
# coding: utf-8

# # Stock Sentiment Analysis
# 
# Check out the video for full details.

# ## Final Code
# Here is the final code:
# This section is only importable in the backtester
from quantopian.algorithm import attach_pipeline, pipeline_output

# General pipeline imports
from quantopian.pipeline import Pipeline
from quantopian.pipeline.factors import AverageDollarVolume

# Using the free sample in your pipeline algo
from quantopian.pipeline.data.accern import alphaone_free

def initialize(context):
    # Schedule our rebalance function to run at the start of each week.
    schedule_function(my_rebalance, date_rules.every_day())
    attach_pipeline(make_pipeline(), "pipeline")

def make_pipeline():
    # Screen out penny stocks and low liquidity securities.
    dollar_volume = AverageDollarVolume(window_length=20)
    is_liquid = dollar_volume.rank(ascending=False) < 1000
 
    # Add pipeline factors
    impact = alphaone_free.impact_score.latest
    sentiment = alphaone_free.article_sentiment.latest

    return Pipeline(columns={
            'impact': impact,
            'sentiment':sentiment,
            },
            screen = is_liquid)
    
    
def before_trading_start(context, data):
    port = pipeline_output('pipeline')
    
    # Grab stocks with 100 impact and >0.5 sentiment and go long.
    context.longs = port[(port['impact']==100) & (port['sentiment']>0.75)].index.tolist()
    
    # Grab stocks with 100 impact and <-0.5 sentiment and go long.
    context.shorts = port[(port['impact']==100) & (port['sentiment']< -0.75)].index.tolist()
    context.long_weight, context.short_weight = my_compute_weights(context)


def my_compute_weights(context):
    # Compute even target weights for our long positions and short positions.
    long_weight = 0.5 / len(context.longs)
    short_weight = -0.5 / len(context.shorts)
    return long_weight, short_weight


def my_rebalance(context, data):
    for security in context.portfolio.positions:
        if security not in context.longs and security not in context.shorts and data.can_trade(security):
            order_target_percent(security, 0)

    for security in context.longs:
        if data.can_trade(security):
            order_target_percent(security, context.long_weight)

    for security in context.shorts:
        if data.can_trade(security):
            order_target_percent(security, context.short_weight)
    
    
    

    

