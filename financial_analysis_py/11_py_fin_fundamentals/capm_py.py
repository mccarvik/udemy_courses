#!/usr/bin/env python
# coding: utf-8
# # CAPM - Capital Asset Pricing Model 
# 
# Watch the video for the full overview.
# 
# Portfolio Returns:
# ## $r_p(t) = \sum\limits_{i}^{n}w_i r_i(t)$
# Market Weights:
# ## $ w_i = \frac{MarketCap_i}{\sum_{j}^{n}{MarketCap_j}} $
# 
# ### CAPM of a portfolio
# 
# ## $ r_p(t) = \beta_pr_m(t) + \sum\limits_{i}^{n}w_i \alpha_i(t)$
# Model CAPM as a simple linear regression
import pdb, sys
from scipy import stats
# help(stats.linregress)
import pandas as pd
import pandas_datareader as web
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/11_py_fin_fundamentals/figs/'

spy_etf = pd.read_csv('SPY.csv',index_col='Date',parse_dates=True)
print(spy_etf.info())
print(spy_etf.head())
start = pd.to_datetime('2012-01-04')
end = pd.to_datetime('2016-12-18')
aapl = pd.read_csv('AAPL_CLOSE',index_col='Date',parse_dates=True)
aapl = aapl[start:end]
spy_etf = spy_etf[start:end]
print(aapl.head())

import matplotlib.pyplot as plt
aapl['Adj. Close'].plot(label='AAPL',figsize=(10,8))
spy_etf['Close'].plot(label='SPY Index')
plt.legend()
plt.savefig(PATH + 'spy_aapl.png', dpi=300)
plt.close()

# ## Compare Cumulative Return
aapl['Cumulative'] = aapl['Adj. Close']/aapl['Adj. Close'].iloc[0]
spy_etf['Cumulative'] = spy_etf['Close']/spy_etf['Close'].iloc[0]

aapl['Cumulative'].plot(label='AAPL',figsize=(10,8))
spy_etf['Cumulative'].plot(label='SPY Index')
plt.legend()
plt.title('Cumulative Return')
plt.savefig(PATH + 'cum_ret.png', dpi=300)
plt.close()

# ## Get Daily Return
aapl['Daily Return'] = aapl['Adj. Close'].pct_change(1)
spy_etf['Daily Return'] = spy_etf['Close'].pct_change(1)

pdb.set_trace()
plt.scatter(aapl['Daily Return'],spy_etf['Daily Return'],alpha=0.3)
plt.savefig(PATH + 'daily_ret_scatter.png', dpi=300)
plt.close()

aapl['Daily Return'].hist(bins=100)
spy_etf['Daily Return'].hist(bins=100)
plt.savefig(PATH + 'daily_ret_hist.png', dpi=300)
plt.close()

beta,alpha,r_value,p_value,std_err = stats.linregress(aapl['Daily Return'].iloc[1:],spy_etf['Daily Return'].iloc[1:])
print(beta)
print(alpha)
print(r_value)

# ## What if our stock was completely related to SP500?
print(spy_etf['Daily Return'].head())

import numpy as np
noise = np.random.normal(0,0.001,len(spy_etf['Daily Return'].iloc[1:]))
print(noise)
print(spy_etf['Daily Return'].iloc[1:] + noise)

beta,alpha,r_value,p_value,std_err = stats.linregress(spy_etf['Daily Return'].iloc[1:]+noise,spy_etf['Daily Return'].iloc[1:])
print(beta)
print(alpha)
