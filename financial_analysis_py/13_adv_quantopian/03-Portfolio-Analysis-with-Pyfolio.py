#!/usr/bin/env python
# coding: utf-8

# # PyFolio Portfolio Analysis

# In[24]:


import pyfolio as pf
import matplotlib.pyplot as plt
import empyrical


# ## Set A Benchmark Algo for SPY

# In[ ]:


def initialize(context):
    context.spy = sid(8554)

    
    set_max_leverage(1.01)
    
    schedule_function(rebalance,date_rules.every_day(),time_rules.market_open())
    
def rebalance(context,data):
    order_target_percent(context.spy,1)


# In[41]:


# Get benchmark returns
benchmark_rets = get_backtest('5986c511c94d014fc81acf7b')


# In[42]:


bm_returns = benchmark_rets.daily_performance['returns']
bm_positions = benchmark_rets.pyfolio_positions
bm_transactions = benchmark_rets.pyfolio_transactions


# ### Use Algo from Leverage Lecture

# In[43]:


# Use same algo as in the Leverage Lecture!
bt = get_backtest('5986b969dbab994fa4264696')


# In[44]:


bt_returns = bt.daily_performance['returns']
bt_positions = bt.pyfolio_positions
bt_transactions = bt.pyfolio_transactions


# In[45]:


bt_returns.plot()


# In[46]:


empyrical.beta(bt_returns,bm_returns)


# # PyFolio Plots

# In[47]:


benchmark_rets = bm_returns


# In[48]:


# Cumulative Returns
plt.subplot(2,1,1)
pf.plotting.plot_rolling_returns(bt_returns, benchmark_rets)

# Daily, Non-Cumulative Returns
plt.subplot(2,1,2)
pf.plotting.plot_returns(bt_returns)
plt.tight_layout()


# In[49]:


fig = plt.figure(1)
plt.subplot(1,3,1)
pf.plot_annual_returns(bt_returns)
plt.subplot(1,3,2)
pf.plot_monthly_returns_dist(bt_returns)
plt.subplot(1,3,3)
pf.plot_monthly_returns_heatmap(bt_returns)
plt.tight_layout()
fig.set_size_inches(15,5)


# In[50]:


pf.plot_return_quantiles(bt_returns);


# In[51]:


pf.plot_rolling_beta(bt_returns, benchmark_rets);


# In[52]:


pf.plot_rolling_sharpe(bt_returns);


# In[53]:


pf.plot_rolling_fama_french(bt_returns);


# In[54]:


pf.plot_drawdown_periods(bt_returns);


# In[55]:


pf.plot_drawdown_underwater(bt_returns);


# In[56]:


pf.plot_gross_leverage(bt_returns, bt_positions);


# In[57]:


pos_percent = pf.pos.get_percent_alloc(bt_positions)
pf.plotting.show_and_plot_top_positions(bt_returns, pos_percent);


# In[58]:


pf.plot_turnover(bt_returns, bt_transactions, bt_positions);


# In[59]:


pf.plotting.plot_daily_turnover_hist(bt_transactions, bt_positions);


# In[60]:


pf.plotting.plot_daily_volume(bt_returns, bt_transactions);


# In[61]:


pf.create_round_trip_tear_sheet(bt_returns, bt_positions, bt_transactions);

