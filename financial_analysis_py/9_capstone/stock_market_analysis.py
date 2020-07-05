#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___
# <center>*Copyright Pierian Data 2017*</center>
# <center>*For more information, visit us at www.pieriandata.com*</center>

# # Stock Market Analysis Project - SOLUTIONS
# 
# Welcome to your first capstone project! This project is meant to cap off the 
# first half of the course, which mainly dealt with learning the libraries that 
# we use in this course, the second half of the course will deal a lot more with 
# quantitative trading techniques and platforms.
# 
# We'll be analyzing stock data related to a few car companies, from Jan 1 2012 
# to Jan 1 2017. Keep in mind that this project is mainly just to practice your 
# skills with matplotlib, pandas, and numpy. Don't infer financial trading
# advice from the analysis we do here!
# 
# ### Part 0: Import
# 
# ** Import the various libraries you will need-you can always just come back up
# here or import as you go along :) **
import sys, pdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/9_capstone/figs/'

# ____
# ## Part 1: Getting the Data
# 
# ### Tesla Stock (Ticker: TSLA on the NASDAQ)
# 
# **  *Note! Not everyone will be working on a computer that will give them
# open access to download the stock information using pandas_datareader 
# (firewalls, admin permissions, etc...). Because of this, the csv file for 
# the Tesla is provided in a data folder inside this folder. It is called 
# Tesla_Stock.csv. Feel free to just use this with read_csv! **
# 
# ** Use pandas_datareader to obtain the historical stock information for
# Tesla from Jan 1, 2012 to Jan 1, 2017.**
# 
# 
import pandas_datareader
import datetime
import pandas_datareader.data as web
start = datetime.datetime(2012, 1, 1)
end = datetime.datetime(2017, 1, 1)
# tesla = web.DataReader("TSLA", 'google', start, end)
tesla = pd.read_csv('./Tesla_Stock.csv',index_col='Date',parse_dates=True)
tesla = tesla[start:end]

print(tesla.head())
tesla.to_csv('Tesla_Stock_save.csv')

# ### Other Car Companies
# 
# ** Repeat the same steps to grab data for Ford and GM (General Motors), **
# ford = web.DataReader("F", 'google', start, end)
# gm = web.DataReader("GM",'google',start,end)
ford = pd.read_csv('./Ford_Stock.csv',index_col='Date',parse_dates=True)[start:end]
gm = pd.read_csv('./GM_Stock.csv',index_col='Date',parse_dates=True)[start:end]

print(ford.head())
ford.to_csv('Ford_Stock_save.csv')
print(gm.head())
gm.to_csv('GM_Stock_save.csv')

# ## Part 2: Visualizing the Data
# 
# ** Time to visualize the data. **
# 
# ** Follow along and recreate the plots below according to the instructions 
# and explanations. **
# ____
# 
# ** Recreate this linear plot of all the stocks' Open price ! Hint: For the
# legend, use label parameter and plt.legend()**
tesla['Open'].plot(label='Tesla',figsize=(16,8),title='Open Price')
gm['Open'].plot(label='GM')
ford['Open'].plot(label='Ford')
plt.legend()
plt.savefig(PATH + 'cars_price.png', dpi=300)
plt.close()

# ____
# ** Plot the Volume of stock traded each day.**
tesla['Volume'].plot(label='Tesla',figsize=(16,8),title='Volume Traded')
gm['Volume'].plot(label='gm')
ford['Volume'].plot(label='ford')
plt.legend()
plt.savefig(PATH + 'cars_vol.png', dpi=300)
plt.close()

# ** Interesting, looks like Ford had a really big spike somewhere in late 
# 2013. What was the date of this maximum trading volume for Ford?**
# 
# **Bonus: What happened that day? **
print(ford['Volume'].argmax())

# What happened:
# http://money.cnn.com/2013/12/18/news/companies/ford-profit/
# https://www.usatoday.com/story/money/cars/2013/12/18/ford-2014-profit-warning/4110015/
# https://media.ford.com/content/dam/fordmedia/North%20America/US/2014/01/28/4QFinancials.pdf
# ____

# ** The Open Price Time Series Visualization makes Tesla look like its always 
# been much more valuable as a company than GM and Ford. But to really understand
# this we would need to look at the total market cap of the company, not just the
# stock price. Unfortunately our current data doesn't have that information of 
# total units of stock present. But what we can do as a simple calcualtion to 
# try to represent total money traded would be to multply the Volume column by
# the Open price. Remember that this still isn't the actual Market Cap, its just
# a visual representation of the total amount of money being traded around using
# the time series. (e.g. 100 units of stock at \$10 each versus 100000 units of 
# stock at $1 each)**
# ** Create a new column for each dataframe called "Total Traded" which is the 
# Open Price multiplied by the Volume Traded.**
tesla['Total Traded'] = tesla['Open']*tesla['Volume']
ford['Total Traded'] = ford['Open']*ford['Volume']
gm['Total Traded'] = gm['Open']*gm['Volume']

# ** Plot this "Total Traded" against the time index.**
tesla['Total Traded'].plot(label='Tesla',figsize=(16,8))
gm['Total Traded'].plot(label='GM')
ford['Total Traded'].plot(label='Ford')
plt.legend()
plt.ylabel('Total Traded')
plt.savefig(PATH + 'total_traded.png', dpi=300)
plt.close()

# ** Interesting, looks like there was huge amount of money traded for Tesla 
# somewhere in early 2014. What date was that and what happened? **
print(tesla['Total Traded'].argmax())
# new method
print(tesla['Total Traded'].idxmax())

# http://money.cnn.com/2014/02/25/investing/tesla-record-high/
# https://blogs.wsj.com/moneybeat/2014/02/25/tesla-shares-surge-on-morgan-stanley-report/
# https://www.washingtonpost.com/news/wonk/wp/2014/02/25/teslas-stock-is-up-644-why-it-may-not-last/
# http://www.cnbc.com/2014/02/25/tesla-soars-ford-falls-in-consumer-reports-study.html

# ____

# ** Let's practice plotting out some MA (Moving Averages). Plot out the MA50 and MA200 for GM. **
gm['MA50'] = gm['Open'].rolling(50).mean()
gm['MA200'] = gm['Open'].rolling(200).mean()
gm[['Open','MA50','MA200']].plot(label='gm',figsize=(16,8))
plt.savefig(PATH + 'mvg_avg.png', dpi=300)
plt.close()

# ______
# ** Finally lets see if there is a relationship between these stocks, after all, 
# they are all related to the car industry. We can see this easily through a 
# scatter matrix plot. Import scatter_matrix from pandas.plotting and use it to 
# create a scatter matrix plot of all the stocks'opening price. You may need to 
# rearrange the columns into a new single dataframe. Hints and info can be found 
# here: https://pandas.pydata.org/pandas-docs/stable/visualization.html#scatter-matrix-plot **
from pandas.plotting import scatter_matrix
car_comp = pd.concat([tesla['Open'],gm['Open'],ford['Open']],axis=1)
car_comp.columns = ['Tesla Open','GM Open','Ford Open']

# You can use a semi-colon to remove the axes print outs
# scatter_matrix(car_comp,figsize=(8,8),alpha=0.2,hist_kwds={'bins':50});
# plt.savefig(PATH + 'scatter_mat.png', dpi=300)
# plt.close()

# _____
# ### Bonus Visualization Task! (Note: This is hard!)
# **Let's now create a candlestick chart! Watch the video if you get stuck on 
# trying to recreate this visualization, there are quite a few steps 
# involved!Refer to the video to understand how to interpret and read this 
# chart. Hints: https://matplotlib.org/examples/pylab_examples/finance_demo.html**
# 
# ** Create a CandleStick chart for Ford in January 2012 (too many dates won't look good for a candlestick chart)**
import mplfinance as mpf
from matplotlib.dates import DateFormatter, date2num, WeekdayLocator, DayLocator, MONDAY

# Rest the index to get a column of January Dates
ford_reset = ford.loc['2012-01':'2012-01'].reset_index()

# Create a new column of numerical "date" values for matplotlib to use
ford_reset['date_ax'] = ford_reset['Date'].apply(lambda date: date2num(date))
ford_values = [tuple(vals) for vals in ford_reset[['date_ax', 'Open', 'High', 'Low', 'Close']].values]

mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
alldays = DayLocator()              # minor ticks on the days
weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
dayFormatter = DateFormatter('%d')      # e.g., 12

#Plot it
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_formatter(weekFormatter)
# original that is deprecated
# from matplotlib.finance import candlestick_ohlc
# candlestick_ohlc(ax, ford_values, width=0.6, colorup='g',colordown='r');

# not sure how to pass axises in with new mpf
mpf.plot(ford.dropna(), type='candle', style='charles')
plt.savefig(PATH + 'candle.png', dpi=300)
plt.close()
sys.exit()
# ____
# # Part 3: Basic Financial Analysis
# 
# Now it is time to focus on a few key financial calculations. This will serve 
# as your transition to the second half of the course. All you need to do is 
# follow along with the instructions, this will mainly be an exercise in 
# converting a mathematical equation or concept into code using python and 
# pandas, something we will do often when working with quantiative data! If 
# you feel very lost in this section, don't worry! Just go to the solutions 
# lecture and treat it as a code-along lecture, use whatever style of learning 
# works best for you!
# 
# Let's begin!
# ____

# ## Daily Percentage Change
# First we will begin by calculating the daily percentage change. Daily 
# percentage change is defined by the following formula:
# $ r_t = \frac{p_t}{p_{t-1}} -1$
# This defines r_t (return at time t) as equal to the price at time t divided 
# by the price at time t-1 (the previous day) minus 1. Basically this just 
# informs you of your percent gain (or loss) if you bought the stock on day 
# and then sold it the next day. While this isn't necessarily helpful for 
# attempting to predict future values of the stock, its very helpful in 
# analyzing the volatility of the stock. If daily returns have a wide 
# distribution, the stock is more volatile from one day to the next. Let's 
# calculate the percent returns and then plot them with a histogram, and decide
# which stock is the most stable!

# ** Create a new column for each dataframe called returns. This column will be
# calculated from the Close price column. There are two ways to do this, either 
# a simple calculation using the .shift() method that follows the formula above,
# or you can also use pandas' built in pct_change method. **


# Method 1: Using shift
tesla['returns'] = (tesla['Close'] / tesla['Close'].shift(1) ) - 1


# In[31]:


tesla.head()


# In[32]:


tesla['returns'] = tesla['Close'].pct_change(1)


# In[33]:


tesla.head()


# In[34]:


# Now repeat for the other dataframes
ford['returns'] = ford['Close'].pct_change(1)
gm['returns'] = gm['Close'].pct_change(1)


# In[35]:


ford.head()


# In[36]:


gm.head()


# ** Now plot a histogram of each companies returns. Either do them separately, or stack them on top of each other. Which stock is the most "volatile"? (as judged by the variance in the daily returns we will discuss volatility in a lot more detail in future lectures.)**

# In[37]:


ford['returns'].hist(bins=50)


# In[38]:


gm['returns'].hist(bins=50)


# In[39]:


tesla['returns'].hist(bins=50)


# In[40]:


tesla['returns'].hist(bins=100,label='Tesla',figsize=(10,8),alpha=0.5)
gm['returns'].hist(bins=100,label='GM',alpha=0.5)
ford['returns'].hist(bins=100,label='Ford',alpha=0.5)
plt.legend()


# ** Try also plotting a KDE instead of histograms for another view point. Which stock has the widest plot? **

# In[41]:


tesla['returns'].plot(kind='kde',label='Tesla',figsize=(12,6))
gm['returns'].plot(kind='kde',label='GM')
ford['returns'].plot(kind='kde',label='Ford')
plt.legend()


# ** Try also creating some box plots comparing the returns. **

# In[42]:


box_df = pd.concat([tesla['returns'],gm['returns'],ford['returns']],axis=1)
box_df.columns = ['Tesla Returns',' GM Returns','Ford Returns']
box_df.plot(kind='box',figsize=(8,11),colormap='jet')


# ## Comparing Daily Returns between Stocks
# 
# ** Create a scatter matrix plot to see the correlation between each of the stocks daily returns. This helps answer the questions of how related the car companies are. Is Tesla begin treated more as a technology company rather than a car company by the market?**

# In[43]:


scatter_matrix(box_df,figsize=(8,8),alpha=0.2,hist_kwds={'bins':50});


# ** It looks like Ford and GM do have some sort of possible relationship, let's plot just these two against eachother in scatter plot to view this more closely!**

# In[44]:


box_df.plot(kind='scatter',x=' GM Returns',y='Ford Returns',alpha=0.4,figsize=(10,8))


# ____
# ## Cumulative Daily Returns
# 
# Great! Now we can see which stock was the most wide ranging in daily returns (you should have realized it was Tesla, our original stock price plot should have also made that obvious).
# 
# With daily cumulative returns, the question we are trying to answer is the following, if I invested $1 in the company at the beginning of the time series, how much would is be worth today? This is different than just the stock price at the current day, because it will take into account the daily returns. Keep in mind, our simple calculation here won't take into account stocks that give back a dividend. Let's look at some simple examples:

# Lets us say there is a stock 'ABC' that is being actively traded on an exchange. ABC has the following prices corresponding to the dates given

#     Date                        Price
#     01/01/2018                   10
#     01/02/2018                   15
#     01/03/2018                   20
#     01/04/2018                   25

# **Daily Return** : Daily return is the profit/loss made by the stock compared to the previous day. (This is what ew just calculated above). A value above one indicates profit, similarly a value below one indicates loss. It is also expressed in percentage to convey the information better. (When expressed as percentage, if the value is above 0, the stock had give you profit else loss). So for the above example the daily returns would be

#     Date                         Daily Return                  %Daily Return
#     01/01/2018                 10/10 =  1                          -   
#     01/02/2018                 15/10 =  3/2                       50%
#     01/03/2018                 20/15 =  4/3                       33%
#     01/04/2018                 25/20 =  5/4                       20%

# **Cumulative Return**: While daily returns are useful, it doesn't give the investor a immediate insight into the gains he had made till date, especially if the stock is very volatile. Cumulative return is computed relative to the day investment is made.  If cumulative return is above one, you are making profits else you are in loss. So for the above example cumulative gains are as follows

#     Date                       Cumulative Return         %Cumulative Return
#     01/01/2018                  10/10 =  1                         100 %   
#     01/02/2018                  15/10 =  3/2                       150 %
#     01/03/2018                  20/10 =  2                         200 %
#     01/04/2018                  25/10 =  5/2                       250 %

# The formula for a cumulative daily return is:
# 
# $ i_i = (1+r_t) * i_{t-1} $
# 
# Here we can see we are just multiplying our previous investment at i at t-1 by 1+our percent returns. Pandas makes this very simple to calculate with its cumprod() method. Using something in the following manner:
# 
#     df[daily_cumulative_return] = ( 1 + df[pct_daily_return] ).cumprod()
#     

# ** Create a cumulative daily return column for each car company's dataframe.**

# In[45]:


tesla['Cumulative Return'] = (1 + tesla['returns']).cumprod()


# In[46]:


tesla.head()


# In[47]:


ford['Cumulative Return'] = (1 + ford['returns']).cumprod()
gm['Cumulative Return'] = (1 + gm['returns']).cumprod()


# ** Now plot the Cumulative Return columns against the time series index. Which stock showed the highest return for a $1 invested? Which showed the lowest?**

# In[48]:


tesla['Cumulative Return'].plot(label='Tesla',figsize=(16,8),title='Cumulative Return')
ford['Cumulative Return'].plot(label='Ford')
gm['Cumulative Return'].plot(label='GM')
plt.legend()


# # Great Job!
# 
# That is it for thsi very basic analysis, this concludes this half of the course, which focuses much more on learning the tools of the trade. The second half of the course is where we really dive into functionality designed for time series, quantitative analysis, algorithmic trading, and much more!
