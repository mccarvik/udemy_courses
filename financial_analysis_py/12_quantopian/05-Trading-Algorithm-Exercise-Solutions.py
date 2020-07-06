#!/usr/bin/env python
# coding: utf-8

# # Trading Algorithm Exercise Solutions
# 
# ** This is an extremely open exercise and there are lots of ways to do it! Please feel free to just skip to the solutions to treat it as an example code along. If you attempt the exercise, do not expect the example solution to exactly match up to your solution. You may have performed much better (or much worse)! **
# 
# ## Your Task
# 
# Your manager wants to see if [Bollinger Bands](https://en.wikipedia.org/wiki/Bollinger_Bands) are still a meaningful technical analysis strategy on their own. For this exercise, you will be testing *Johnson and Johnson* sid(4151).Specifically, your manager has decided he wants set 100% of the portfolio to go long when the stock price is below 2 times the 20 day rolling standard deviation subtracted from the 20 day moving average, and go 100% short of the portfolio on that stock when the current price is above 2 times the 20 day rolling standard deviation added on to the 20 day moving average. The check for this signal event should only happen once per day. This is probably a very unreasonable strategy, but the main point of this is to exercise your ability to write out backtest algorithms with Quantopian.
# 
# ## Time Frame
# 
# You should use the following time frame for this exercise (so you can at least have a reasonable comparison to the solutions, but feel free to play around with this!)
# 
# #### BACKTEST START:  Jul-20-2014
# #### BACKTEST END: Jul-20-2017

# In[ ]:


# Setup our variables
def initialize(context):
    context.jj = sid(4151)

    schedule_function(check_bands,date_rules.every_day())
        
def check_bands(context, data):
    
    cur_price = data.current(context.jj,'price')
    
    # Load historical data for the stocks
    prices = data.history(context.jj,'price', 20 , '1d')
    
    avg = prices.mean()
    std = prices.std()
    lower_band = avg - 2*std
    upper_band = avg + 2*std
    
    if cur_price <= lower_band:
        order_target_percent(context.jj, 1.0)
        print('Buying')
        print('Current price is: ' + str(cur_price))
        print("Lower band is: "+str(lower_band))
        
        
    elif cur_price >= upper_band:
        order_target_percent(context.jj, -1.0)
        print('Shorting')
        print('Current price is: ' + str(cur_price))
        print("Upper band is: "+str(upper_band))
    else:
        pass
        
    record(upper=upper_band,
           lower=lower_band,
           mvag_20=avg,
           price=cur_price)

