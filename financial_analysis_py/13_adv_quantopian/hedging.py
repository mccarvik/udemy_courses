#!/usr/bin/env python
# coding: utf-8

# # Hedging
# 
# Make sure to refer to the video for full explanations!
import numpy as np
from statsmodels import regression
import statsmodels.api as sm
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/13_adv_quantopian/figs/'

# Get data for the specified period and stocks
start = '2016-01-01'
end = '2017-01-01'
asset = get_pricing('AAPL', fields='price', start_date=start, end_date=end)
benchmark = get_pricing('SPY', fields='price', start_date=start, end_date=end)

asset_ret = asset.pct_change()[1:]
bench_ret = benchmark.pct_change()[1:]

asset_ret.plot()
bench_ret.plot()
plt.legend()
plt.savefig(PATH + 'asset_v_bench.png', dpi=300)
plt.close()

# ## Regression for Alpha and Beta Values
plt.scatter(bench_ret,asset_ret,alpha=0.6,s=50)
plt.xlabel('SPY Ret')
plt.ylabel('AAPL Ret')
plt.savefig(PATH + 'scatter.png', dpi=300)
plt.close()

AAPL = asset_ret.values
spy = bench_ret.values


# Add a constant (column of 1s for intercept)
spy_constant = sm.add_constant(spy)

# Fit regression to data
model = regression.linear_model.OLS(AAPL,spy_constant).fit()

print(model.params)
alpha , beta = model.params
print(alpha)
print(beta)

# ### Plot Alpha and Beta
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
plt.savefig(PATH + 'scat_line.png', dpi=300)
plt.close()


# ## Implementing the Hedge
hedged = -1*beta*bench_ret + asset_ret

hedged.plot(label='AAPL with Hedge')
bench_ret.plot(alpha=0.5)
asset_ret.plot(alpha=0.5)
plt.legend()
plt.savefig(PATH + 'hedge.png', dpi=300)
plt.close()


# #### What happens if there is a big market drop?
hedged.plot(label='AAPL with Hedge')
bench_ret.plot()
asset_ret.plot()
plt.xlim(['2016-06-01','2016-08-01'])
plt.legend()
plt.savefig(PATH + 'market_drop.png', dpi=300)
plt.close()

# ### Effects of Hedging
def alpha_beta(benchmark_ret,stock):
    benchmark = sm.add_constant(benchmark_ret)
    model = regression.linear_model.OLS(stock,benchmark).fit()
    return model.params[0], model.params[1]


# ** 2016-2017 Alpha and Beta **
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
# Create hedged portfolio and compute alpha and beta
portfolio = -1*beta2016*benchmark_ret2016 + asset_ret2016
alpha, beta = alpha_beta(benchmark_ret2016,portfolio)
print('Portfolio with Alphas and Betas:')
print('alpha: ' + str(alpha))
print('beta: ' + str(beta))

# Plot the returns of the portfolio as well as the asset by itself
portfolio.plot(alpha=0.9,label='AAPL with Hedge')
asset_ret2016.plot(alpha=0.5);
benchmark_ret2016.plot(alpha=0.5)
plt.ylabel("Daily Return")
plt.legend();
plt.savefig(PATH + 'port_ret.png', dpi=300)
plt.close()

print(portfolio.mean())
print(asset_ret2016.mean())
print(portfolio.std())
print(asset_ret2016.std())

# _____
# ** 2017 Based Figures **
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
# Create hedged portfolio and compute alpha and beta
portfolio = -1*beta2016*benchmark_ret2017 + asset_ret2017

alpha, beta = alpha_beta(benchmark_ret2017,portfolio)
print('Portfolio with Alphas and Betas Out of Sample:')
print('alpha: ' + str(alpha))
print('beta: ' + str(beta))

# Plot the returns of the portfolio as well as the asset by itself
portfolio.plot(alpha=0.9,label='AAPL with Hedge')
asset_ret2017.plot(alpha=0.5);
benchmark_ret2017.plot(alpha=0.5)
plt.ylabel("Daily Return")
plt.legend();
plt.savefig(PATH + 'asset_ret_and_port_ret.png', dpi=300)
plt.close()

# What are the actual effects? Typically sacrificing average returns for less volatility,
# but this is also highly dependent on the security:
print(portfolio.mean())
print(asset_ret2017.mean())
print(portfolio.std())
print(asset_ret2017.std())
