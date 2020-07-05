#!/usr/bin/env python
# coding: utf-8

# # Visualizing Time Series Data
# 
# Let's go through a few key points of creatng nice time visualizations!

# In[1]:
import pdb
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/6_matplotlib/figs/'

# Optional for interactive
# %matplotlib notebook (watch video for full details)
mcdon = pd.read_csv('mcdonalds.csv',index_col='Date',parse_dates=True)
print(mcdon.head())
# Not Good!
mcdon.plot()
plt.savefig(PATH + 'mcd_distorted.png', dpi=300)
plt.close()

mcdon['Adj. Close'].plot()
plt.savefig(PATH + 'mcd_adj_close.png', dpi=300)
plt.close()
mcdon['Adj. Volume'].plot()
plt.savefig(PATH + 'mdc_adj_vol.png', dpi=300)
plt.close()

mcdon['Adj. Close'].plot(figsize=(12,8))
plt.savefig(PATH + 'mcd_adj_close_wide.png', dpi=300)
plt.close()

mcdon['Adj. Close'].plot(figsize=(12,8))
plt.ylabel('Close Price')
plt.xlabel('Overwrite Date Index')
plt.title('Mcdonalds')
plt.savefig(PATH + 'mcd_labels.png', dpi=300)
plt.close()

mcdon['Adj. Close'].plot(figsize=(12,8),title='Pandas Title')
plt.savefig(PATH + 'mcd_titles.png', dpi=300)
plt.close()

# # Plot Formatting
# ## X Limits
mcdon['Adj. Close'].plot(xlim=['2007-01-01','2009-01-01'])
plt.savefig(PATH + 'mcd_xlim.png', dpi=300)
plt.close()
mcdon['Adj. Close'].plot(xlim=['2007-01-01','2009-01-01'],ylim=[0,50])
plt.savefig(PATH + 'mcd_ylim.png', dpi=300)
plt.close()


# ## Color and Style
mcdon['Adj. Close'].plot(xlim=['2007-01-01','2007-05-01'],ylim=[0,40],ls='--',c='r')
plt.savefig(PATH + 'mcd_limstyle.png', dpi=300)
plt.close()

# ## X Ticks
# 
# This is where you will need the power of matplotlib to do heavy lifting if you want some serious customization!
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.dates as dates

idx = mcdon.loc['2007-01-01':'2007-05-01'].index
stock = mcdon.loc['2007-01-01':'2007-05-01']['Adj. Close']
print(idx)
print(stock)

#  ## Basic matplotlib plot
fig, ax = plt.subplots()
ax.plot_date(idx, stock,'-')
plt.savefig(PATH + 'plot_date.png', dpi=300)
plt.tight_layout()
plt.savefig(PATH + 'plot_date_tight.png', dpi=300)
plt.close()

# ## Fix the overlap!
fig, ax = plt.subplots()
ax.plot_date(idx, stock,'-')
fig.autofmt_xdate() # Auto fixes the overlap!
plt.tight_layout()
plt.savefig(PATH + 'plot_date_fix.png', dpi=300)
plt.close()

# ## Customize grid
fig, ax = plt.subplots()
ax.plot_date(idx, stock,'-')
ax.yaxis.grid(True)
ax.xaxis.grid(True)
fig.autofmt_xdate() # Auto fixes the overlap!
plt.tight_layout()
plt.savefig(PATH + 'custom_grid.png', dpi=300)
plt.close()

# ## Format dates on Major Axis
fig, ax = plt.subplots()
ax.plot_date(idx, stock,'-')

# Grids
ax.yaxis.grid(True)
ax.xaxis.grid(True)

# Major Axis
# Locating
ax.xaxis.set_major_locator(dates.MonthLocator())
# Formatting
ax.xaxis.set_major_formatter(dates.DateFormatter('%b\n%Y'))
fig.autofmt_xdate() # Auto fixes the overlap!
plt.tight_layout()
plt.savefig(PATH + 'dates_major_axis.png', dpi=300)
plt.close()


fig, ax = plt.subplots()
ax.plot_date(idx, stock,'-')

# Grids
ax.yaxis.grid(True)
ax.xaxis.grid(True)

# Major Axis
ax.xaxis.set_major_locator(dates.MonthLocator())
ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n\n\n%Y--%B'))

fig.autofmt_xdate() # Auto fixes the overlap!
plt.tight_layout()
plt.savefig(PATH + 'major_axis_2.png', dpi=300)
plt.close()

# ## Minor Axis
fig, ax = plt.subplots()
ax.plot_date(idx, stock,'-')

# Major Axis
ax.xaxis.set_major_locator(dates.MonthLocator())
ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n%Y--%B'))

# Minor Axis
ax.xaxis.set_minor_locator(dates.WeekdayLocator())
ax.xaxis.set_minor_formatter(dates.DateFormatter('%d'))

# Grids
ax.yaxis.grid(True)
ax.xaxis.grid(True)

fig.autofmt_xdate() # Auto fixes the overlap!
plt.tight_layout()
plt.savefig(PATH + 'minor_axis.png', dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10,8))
ax.plot_date(idx, stock,'-')

# Major Axis
ax.xaxis.set_major_locator(dates.WeekdayLocator(byweekday=1))
ax.xaxis.set_major_formatter(dates.DateFormatter('%B-%d-%a'))
# Grids
ax.yaxis.grid(True)
ax.xaxis.grid(True)
fig.autofmt_xdate() # Auto fixes the overlap!
plt.tight_layout()
plt.savefig(PATH + 'minor_axis_2.png', dpi=300)
plt.close()
