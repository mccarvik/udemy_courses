#!/usr/bin/env python
# coding: utf-8

# # Portfolio Optimization

# “Modern Portfolio Theory (MPT), a hypothesis put forth by Harry Markowitz in his 
# paper “Portfolio Selection,” (published in 1952 by the Journal of Finance) is an 
# investment theory based on the idea that risk-averse investors can construct
# portfolios to optimize or maximize expected return based on a given level of 
# market risk, emphasizing that risk is an inherent part of higher reward. It is 
# one of the most important and influential economic theories dealing with finance 
# and investment.

# ## Monte Carlo Simulation for Optimization Search
# 
# 
# We could randomly try to find the optimal portfolio balance using Monte Carlo 
# simulation
import pdb, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/11_py_fin_fundamentals/figs/'
# Download and get Daily Returns
aapl = pd.read_csv('AAPL_CLOSE',index_col='Date',parse_dates=True)
cisco = pd.read_csv('CISCO_CLOSE',index_col='Date',parse_dates=True)
ibm = pd.read_csv('IBM_CLOSE',index_col='Date',parse_dates=True)
amzn = pd.read_csv('AMZN_CLOSE',index_col='Date',parse_dates=True)

stocks = pd.concat([aapl,cisco,ibm,amzn],axis=1)
stocks.columns = ['aapl','cisco','ibm','amzn']
print(stocks.head())
mean_daily_ret = stocks.pct_change(1).mean()
print(mean_daily_ret)
print(stocks.pct_change(1).corr())

# # Simulating Thousands of Possible Allocations
print(stocks.head())
stock_normed = stocks/stocks.iloc[0]
stock_normed.plot()
plt.savefig(PATH + 'stock_normed.png', dpi=300)
plt.close()

stock_daily_ret = stocks.pct_change(1)
print(stock_daily_ret.head())

# ## Log Returns vs Arithmetic Returns
# 
# We will now switch over to using log returns instead of arithmetic returns, 
# for many of our use cases they are almost the same,but most technical analyses 
# require detrending/normalizing the time series and using log returns is a nice 
# way to do that.
# Log returns are convenient to work with in many of the algorithms we will encounter.
# 
# For a full analysis of why we use log returns, check [this great article](https://quantivity.wordpress.com/2011/02/21/why-log-returns/).
# 
log_ret = np.log(stocks/stocks.shift(1))
print(log_ret.head())
log_ret.hist(bins=100,figsize=(12,6));
plt.tight_layout()
plt.savefig(PATH + 'log_hist.png', dpi=300)
plt.close()

print(log_ret.describe().transpose())
print(log_ret.mean() * 252)

# Compute pairwise covariance of columns
print(log_ret.cov())
print(log_ret.cov()*252) # multiply by days


# ## Single Run for Some Random Allocation
# Set seed (optional)
np.random.seed(101)

# Stock Columns
print('Stocks')
print(stocks.columns)
print('\n')

# Create Random Weights
print('Creating Random Weights')
weights = np.array(np.random.random(4))
print(weights)
print('\n')

# Rebalance Weights
print('Rebalance to sum to 1.0')
weights = weights / np.sum(weights)
print(weights)
print('\n')

# Expected Return
print('Expected Portfolio Return')
exp_ret = np.sum(log_ret.mean() * weights) *252
print(exp_ret)
print('\n')

# Expected Variance
print('Expected Volatility')
exp_vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))
print(exp_vol)
print('\n')

# Sharpe Ratio
SR = exp_ret/exp_vol
print('Sharpe Ratio')
print(SR)

# Great! Now we can just run this many times over!
num_ports = 5000
all_weights = np.zeros((num_ports,len(stocks.columns)))
ret_arr = np.zeros(num_ports)
vol_arr = np.zeros(num_ports)
sharpe_arr = np.zeros(num_ports)

for ind in range(num_ports):

    # Create Random Weights
    weights = np.array(np.random.random(4))

    # Rebalance Weights
    weights = weights / np.sum(weights)
    
    # Save Weights
    all_weights[ind,:] = weights

    # Expected Return
    ret_arr[ind] = np.sum((log_ret.mean() * weights) *252)

    # Expected Variance
    vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))

    # Sharpe Ratio
    sharpe_arr[ind] = ret_arr[ind]/vol_arr[ind]

print(sharpe_arr.max())
print(sharpe_arr.argmax())
print(all_weights[1419,:])
max_sr_ret = ret_arr[1419]
max_sr_vol = vol_arr[1419]


# ## Plotting the data
plt.figure(figsize=(12,8))
plt.scatter(vol_arr,ret_arr,c=sharpe_arr,cmap='plasma')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Return')

# Add red dot for max SR
plt.scatter(max_sr_vol,max_sr_ret,c='red',s=50,edgecolors='black')
plt.savefig(PATH + 'scatter_mc.png', dpi=300)
plt.close()

# # Mathematical Optimization
# 
# There are much better ways to find good allocation weights than just guess and check! We can use optimization functions to find the ideal weights mathematically!
# ### Functionalize Return and SR operations

def get_ret_vol_sr(weights):
    """
    Takes in weights, returns array or return,volatility, sharpe ratio
    """
    weights = np.array(weights)
    ret = np.sum(log_ret.mean() * weights) * 252
    vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))
    sr = ret/vol
    return np.array([ret,vol,sr])

from scipy.optimize import minimize
# To fully understand all the parameters, check out:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
# help(minimize)
# Optimization works as a minimization function, since we actually want to maximize 
# the Sharpe Ratio, we will need to turn it negative so we can minimize the negative
# sharpe (same as maximizing the postive sharpe)

def neg_sharpe(weights):
    return  get_ret_vol_sr(weights)[2] * -1

# Contraints
def check_sum(weights):
    '''
    Returns 0 if sum of weights is 1.0
    '''
    return np.sum(weights) - 1

# By convention of minimize function it should be a function that returns zero for conditions
cons = ({'type':'eq','fun': check_sum})
# 0-1 bounds for each weight
bounds = ((0, 1), (0, 1), (0, 1), (0, 1))
# Initial Guess (equal distribution)
init_guess = [0.25,0.25,0.25,0.25]
# Sequential Least SQuares Programming (SLSQP).
opt_results = minimize(neg_sharpe,init_guess,method='SLSQP',bounds=bounds,constraints=cons)

print(opt_results)
print(opt_results.x)
print(get_ret_vol_sr(opt_results.x))

# # All Optimal Portfolios (Efficient Frontier)
# 
# The efficient frontier is the set of optimal portfolios that offers the highest 
# expected return for a defined level of risk or the lowest risk for a given level 
# of expected return. Portfolios that lie below the efficient frontier are 
# sub-optimal, because they do not provide enough return for the level of risk. 
# Portfolios that cluster to the right of the efficient frontier are also sub-optimal,
# because they have a higher level of risk for the defined rate of return.
# 
# Efficient Frontier http://www.investopedia.com/terms/e/efficientfrontier
# Our returns go from 0 to somewhere along 0.3
# Create a linspace number of points to calculate x on
frontier_y = np.linspace(0,0.3,20) # Change 100 to a lower number for slower computers!

def minimize_volatility(weights):
    return  get_ret_vol_sr(weights)[1] 

frontier_volatility = []

for possible_return in frontier_y:
    # function for return
    cons = ({'type':'eq','fun': check_sum},
            {'type':'eq','fun': lambda w: get_ret_vol_sr(w)[0] - possible_return})
    
    result = minimize(minimize_volatility,init_guess,method='SLSQP',bounds=bounds,constraints=cons)
    frontier_volatility.append(result['fun'])

plt.figure(figsize=(12,8))
plt.scatter(vol_arr,ret_arr,c=sharpe_arr,cmap='plasma')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Return')
# Add frontier line
plt.plot(frontier_volatility,frontier_y,'g--',linewidth=3)
plt.savefig(PATH + 'frontier.png', dpi=300)
plt.close()
