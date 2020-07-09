#!/usr/bin/env python
# coding: utf-8

# # Hedging
# 
# Make sure to refer to the video for full explanations!

# In[163]:


import numpy as np
from statsmodels import regression
import statsmodels.api as sm
import matplotlib.pyplot as plt


# In[164]:


# Get data for the specified period and stocks
start = '2016-01-01'
end = '2017-01-01'
asset = get_pricing('AAPL', fields='price', start_date=start, end_date=end)
benchmark = get_pricing('SPY', fields='price', start_date=start, end_date=end)


# In[165]:


asset_ret = asset.pct_change()[1:]
bench_ret = benchmark.pct_change()[1:]


# In[166]:


asset_ret.plot()
bench_ret.plot()
plt.legend()


# ## Regression for Alpha and Beta Values

# In[167]:


plt.scatter(bench_ret,asset_ret,alpha=0.6,s=50)
plt.xlabel('SPY Ret')
plt.ylabel('AAPL Ret')


# In[168]:


AAPL = asset_ret.values
spy = bench_ret.values


# In[169]:


# Add a constant (column of 1s for intercept)
spy_constant = sm.add_constant(spy)

# Fit regression to data
model = regression.linear_model.OLS(AAPL,spy_constant).fit()


# In[170]:


model.params


# In[171]:


alpha , beta = model.params


# In[172]:


alpha


# In[173]:


beta


# ### Plot Alpha and Beta

# In[174]:


# Scatter Returns
plt.scatter(bench_ret,asset_ret,alpha=0.6,s=50)

# Fit Line
min_spy = bench_ret.values.min()
max_spy = bench_ret.values.max()

spy_line = np.linspace(min_spy,max_spy,100)
y = spy_line * beta + alpha

plt.plot(spy_line,y,'r')

plt.xlabel('SPY Ret')
plt.ylabel('AAPL Ret')


# ## Implementing the Hedge

# In[175]:


hedged = -1*beta*bench_ret + asset_ret


# In[176]:


hedged.plot(label='AAPL with Hedge')
bench_ret.plot(alpha=0.5)
asset_ret.plot(alpha=0.5)
plt.legend()


# #### What happens if there is a big market drop?

# In[177]:


hedged.plot(label='AAPL with Hedge')
bench_ret.plot()
asset_ret.plot()
plt.xlim(['2016-06-01','2016-08-01'])
plt.legend()


# ### Effects of Hedging

# In[178]:


def alpha_beta(benchmark_ret,stock):
    
    benchmark = sm.add_constant(benchmark_ret)
    
    model = regression.linear_model.OLS(stock,benchmark).fit()
    
    return model.params[0], model.params[1]


# ** 2016-2017 Alpha and Beta **

# In[179]:


# Get the alpha and beta estimates over the last year
start = '2016-01-01'
end = '2017-01-01'

asset2016 = get_pricing('AAPL', fields='price', start_date=start, end_date=end)
benchmark2016 = get_pricing('SPY', fields='price', start_date=start, end_date=end)

asset_ret2016 = asset2016.pct_change()[1:]
benchmark_ret2016 = benchmark2016.pct_change()[1:]

aret_val = asset_ret2016.values
bret_val = benchmark_ret2016.values

alpha2016, beta2016 = alpha_beta(bret_val,aret_val)

print('2016 Based Figures')
print('alpha: ' + str(alpha2016))
print('beta: ' + str(beta2016))


# ** Creating a Portfolio **

# In[180]:


# Create hedged portfolio and compute alpha and beta
portfolio = -1*beta2016*benchmark_ret2016 + asset_ret2016

alpha, beta = alpha_beta(benchmark_ret2016,portfolio)
print('Portfolio with Alphas and Betas:')
print('alpha: ' + str(alpha))
print('beta: ' + str(beta))


# In[181]:


# Plot the returns of the portfolio as well as the asset by itself
portfolio.plot(alpha=0.9,label='AAPL with Hedge')
asset_ret2016.plot(alpha=0.5);
benchmark_ret2016.plot(alpha=0.5)
plt.ylabel("Daily Return")
plt.legend();


# In[182]:


portfolio.mean()


# In[183]:


asset_ret2016.mean()


# In[184]:


portfolio.std()


# In[185]:


asset_ret2016.std()


# _____

# ** 2017 Based Figures **

# In[186]:


# Get data for a different time frame:
start = '2017-01-01'
end = '2017-08-01'

asset2017 = get_pricing('AAPL', fields='price', start_date=start, end_date=end)
benchmark2017 = get_pricing('SPY', fields='price', start_date=start, end_date=end)

asset_ret2017 = asset2017.pct_change()[1:]
benchmark_ret2017 = benchmark2017.pct_change()[1:]

aret_val = asset_ret2017.values
bret_val = benchmark_ret2017.values

alpha2017, beta2017 = alpha_beta(bret_val,aret_val)

print('2016 Based Figures')
print('alpha: ' + str(alpha2017))
print('beta: ' + str(beta2017))


# ** Creating a Portfolio based off 2016 Beta estimate **

# In[187]:


# Create hedged portfolio and compute alpha and beta
portfolio = -1*beta2016*benchmark_ret2017 + asset_ret2017

alpha, beta = alpha_beta(benchmark_ret2017,portfolio)
print 'Portfolio with Alphas and Betas Out of Sample:'
print 'alpha: ' + str(alpha)
print 'beta: ' + str(beta)


# In[188]:


# Plot the returns of the portfolio as well as the asset by itself
portfolio.plot(alpha=0.9,label='AAPL with Hedge')
asset_ret2017.plot(alpha=0.5);
benchmark_ret2017.plot(alpha=0.5)
plt.ylabel("Daily Return")
plt.legend();


# What are the actual effects? Typically sacrificing average returns for less volatility, but this is also highly dependent on the security:

# In[189]:


portfolio.mean()


# In[190]:


asset_ret2017.mean()


# In[191]:


portfolio.std()


# In[192]:


asset_ret2017.std()


# # Great Job!
