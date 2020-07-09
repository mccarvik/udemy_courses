#!/usr/bin/env python
# coding: utf-8

# # Leverage
# 
# Make sure to watch the video and slides for this lecture for the full explanation!
# 
# $ Leverage Ratio = \frac{Debt + Capital Base}{Capital Base}$

# ## Leverage from Algorithm
# 
# Make sure to watch the video for this! Basically run this and grab your own 
# backtestid as shown in the video. More info:
# 
# The get_backtest function provides programmatic access to the results of 
# backtests run on the Quantopian platform. It takes a single parameter, the ID
# of a backtest for which results are desired.
# 
# You can find the ID of a backtest in the URL of its full results page, which will be of the form:
# 
# https://www.quantopian.com/algorithms/<algorithm_id>/<backtest_id>.  
# 
# You are only entitled to view the backtests that either:
# 
# * 1) you have created
# * 2) you are a collaborator on
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/13_adv_quantopian/figs/'

def initialize(context):
    context.amzn = sid(16841)
    context.ibm = sid(3766)
    
    schedule_function(rebalance,date_rules.every_day(),time_rules.market_open())
    schedule_function(record_vars,date_rules.every_day(),time_rules.market_close())
    
def rebalance(context,data):
    order_target_percent(context.amzn,0.5)
    order_target_percent(context.ibm,-0.5)
    
def record_vars(context,data):
    record(amzn_close=data.current(context.amzn,'close'))
    record(ibm_close=data.current(context.ibm,'close'))
    record(Leverage = context.account.leverage)
    record(Exposure = context.account.net_leverage)


# ## Backtest Info
bt = get_backtest('5986b969dbab994fa4264696')
print(bt.algo_id)
print(bt.recorded_vars)

bt.recorded_vars['Leverage'].plot()
bt.recorded_vars['Exposure'].plot()
plt.savefig(PATH + 'quandl_1.png', dpi=300)
plt.close()

# ##  High Leverage Example
# 
# You can actually specify to borrow on margin (NOT RECOMMENDED)

# In[ ]:


def initialize(context):
    context.amzn = sid(16841)
    context.ibm = sid(3766)
    
    schedule_function(rebalance,date_rules.every_day(),time_rules.market_open())
    schedule_function(record_vars,date_rules.every_day(),time_rules.market_close())
    
def rebalance(context,data):
    order_target_percent(context.ibm,-2.0)
    order_target_percent(context.amzn,2.0)
    
def record_vars(context,data):
    record(amzn_close=data.current(context.amzn,'close'))
    record(ibm_close=data.current(context.ibm,'close'))
    record(Leverage = context.account.leverage)
    record(Exposure = context.account.net_leverage)


# In[15]:


bt = get_backtest('5986bd68ceda5554428a005b')


# In[16]:


bt.recorded_vars['Leverage'].plot()


# ## Set Hard Limit on Leverage
# 
# http://www.zipline.io/appendix.html?highlight=leverage#zipline.api.set_max_leverage

# In[ ]:


def initialize(context):
    context.amzn = sid(16841)
    context.ibm = sid(3766)
    
    set_max_leverage(1.03)
    
    schedule_function(rebalance,date_rules.every_day(),time_rules.market_open())
    schedule_function(record_vars,date_rules.every_day(),time_rules.market_close())
    
def rebalance(context,data):
    order_target_percent(context.ibm,-0.5)
    order_target_percent(context.amzn,0.5)
    
def record_vars(context,data):
    record(amzn_close=data.current(context.amzn,'close'))
    record(ibm_close=data.current(context.ibm,'close'))
    record(Leverage = context.account.leverage)
    record(Exposure = context.account.net_leverage)

