#!/usr/bin/env python
# coding: utf-8

# # Sharpe Ratio and Portfolio Values
import sys, pdb
import pandas as pd
import quandl
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/11_py_fin_fundamentals/figs/'

# ## Create a Portfolio
start = pd.to_datetime('2012-01-01')
end = pd.to_datetime('2017-01-01')

# Grabbing a bunch of tech stocks for our portfolio
# aapl = quandl.get('WIKI/AAPL.11',start_date=start,end_date=end)
# cisco = quandl.get('WIKI/CSCO.11',start_date=start,end_date=end)
# ibm = quandl.get('WIKI/IBM.11',start_date=start,end_date=end)
# amzn = quandl.get('WIKI/AMZN.11',start_date=start,end_date=end)

# Alternative
aapl = pd.read_csv('AAPL_CLOSE',index_col='Date',parse_dates=True)
cisco = pd.read_csv('CISCO_CLOSE',index_col='Date',parse_dates=True)
ibm = pd.read_csv('IBM_CLOSE',index_col='Date',parse_dates=True)
amzn = pd.read_csv('AMZN_CLOSE',index_col='Date',parse_dates=True)

# aapl.to_csv('AAPL_CLOSE')
# cisco.to_csv('CISCO_CLOSE')
# ibm.to_csv('IBM_CLOSE')
# amzn.to_csv('AMZN_CLOSE')

# ## Normalize Prices
# 
# This is the same as cumulative daily returns
# Example
print(aapl.iloc[0]['Adj. Close'])

for stock_df in (aapl,cisco,ibm,amzn):
    stock_df['Normed Return'] = stock_df['Adj. Close']/stock_df.iloc[0]['Adj. Close']

print(aapl.head())
print(aapl.tail())

# ## Allocations
# 
# Let's pretend we had the following allocations for our total portfolio:
# 
# * 30% in Apple
# * 20% in Google/Alphabet
# * 40% in Amazon
# * 10% in IBM
# 
# Let's have these values be reflected by multiplying our Norme Return by out Allocations
for stock_df,allo in zip([aapl,cisco,ibm,amzn],[.3,.2,.4,.1]):
    stock_df['Allocation'] = stock_df['Normed Return']*allo

print(aapl.head())

# ## Investment
# 
# Let's pretend we invested a million dollars in this portfolio
for stock_df in [aapl,cisco,ibm,amzn]:
    stock_df['Position Values'] = stock_df['Allocation']*1000000

# ## Total Portfolio Value
portfolio_val = pd.concat([aapl['Position Values'],cisco['Position Values'],ibm['Position Values'],amzn['Position Values']],axis=1)
print(portfolio_val.head())

portfolio_val.columns = ['AAPL Pos','CISCO Pos','IBM Pos','AMZN Pos']
print(portfolio_val.head())

portfolio_val['Total Pos'] = portfolio_val.sum(axis=1)
print(portfolio_val.head())

portfolio_val['Total Pos'].plot(figsize=(10,8))
plt.title('Total Portfolio Value')
plt.savefig(PATH + 'total_pos.png', dpi=300)
plt.close()

portfolio_val.drop('Total Pos',axis=1).plot(kind='line')
plt.savefig(PATH + 'all_pos.png', dpi=300)
plt.close()
print(portfolio_val.tail())

# # Portfolio Statistics
# ### Daily Returns
portfolio_val['Daily Return'] = portfolio_val['Total Pos'].pct_change(1)

# ### Cumulative Return
cum_ret = 100 * (portfolio_val['Total Pos'][-1]/portfolio_val['Total Pos'][0] -1 )
print('Our return {} was percent!'.format(cum_ret))

# ### Avg Daily Return
print(portfolio_val['Daily Return'].mean())

# ### Std Daily Return
print(portfolio_val['Daily Return'].std())

portfolio_val['Daily Return'].plot(kind='kde')
plt.savefig(PATH + 'kde.png', dpi=300)
plt.close()

# # Sharpe Ratio
# 
# The Sharpe Ratio is a measure for calculating risk-adjusted return, and this 
# ratio has become the industry standard for such calculations. 
# 
# Sharpe ratio = (Mean portfolio return − Risk-free rate)/Standard deviation of 
# portfolio return
# 
# The original Sharpe Ratio
# 
# Annualized Sharpe Ratio = K-value * SR
# 
# K-values for various sampling rates:
# 
# * Daily = sqrt(252)
# * Weekly = sqrt(52)
# * Monthly = sqrt(12)
# 
# Since I'm based in the USA, I will use a very low risk-free rate (the rate
# you would get if you just put your money in a bank, its currently very low 
# in the USA, let's just say its ~0% return). If you are in a different country
# with higher rates for your trading currency, you can use this trick to convert
# a yearly rate with a daily rate:
# 
# daily_rate = ((1.0 + yearly_rate)**(1/252))-1
# 
# Other values people use are things like the 3-month treasury bill or [LIBOR](http://www.investopedia.com/terms/l/libor.asp).
# 
# Read more: Sharpe Ratio http://www.investopedia.com/terms/s/sharperatio
SR = portfolio_val['Daily Return'].mean()/portfolio_val['Daily Return'].std()
print(SR)
# annualize it
ASR = (252**0.5)*SR
print(ASR)

print(portfolio_val['Daily Return'].std())
print(portfolio_val['Daily Return'].mean())

portfolio_val['Daily Return'].plot('kde')
plt.savefig(PATH + 'kde_daily.png', dpi=300)
plt.close()

aapl['Adj. Close'].pct_change(1).plot('kde')
ibm['Adj. Close'].pct_change(1).plot('kde')
amzn['Adj. Close'].pct_change(1).plot('kde')
cisco['Adj. Close'].pct_change(1).plot('kde')
plt.savefig(PATH + 'kde_ind.png', dpi=300)
plt.close()

import numpy as np
np.sqrt(252)* (np.mean(.001-0.0002)/.001)
