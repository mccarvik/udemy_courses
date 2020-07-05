#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../../Pierian_Data_Logo.png' /></a>
# ___
# # Pandas Built-in Data Visualization
# 
# In this lecture we will learn about pandas built-in capabilities for data 
# visualization! It's built-off of matplotlib, but it baked into pandas for 
# easier usage!  
# 
# Let's take a look!

# ## Imports
import pdb
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/6_matplotlib/figs/'

# ## The Data
# 
# There are some fake data csv files you can read in as dataframes:
df1 = pd.read_csv('df1',index_col=0)
df2 = pd.read_csv('df2')

# ## Style Sheets
# 
# Matplotlib has [style sheets](http://matplotlib.org/gallery.html#style_sheets) you 
# can use to make your plots look a little nicer. These style sheets include 
# plot_bmh,plot_fivethirtyeight,plot_ggplot and more. They basically create a 
# set of style rules that your plots follow. I recommend using them, they make 
# all your plots have the same look and feel more professional. You can even 
# create your own if you want your company's plots to all have the same look 
# (it is a bit tedious to create on though).
# 
# Here is how to use them.
# 
# **Before plt.style.use() your plots look like this:**
df1['A'].hist()
plt.savefig(PATH + 'hist.png', dpi=300)
plt.close()

# Call the style:
plt.style.use('ggplot')

# Now your plots look like this:
df1['A'].hist()
plt.savefig(PATH + 'hist2.png', dpi=300)
plt.close()

plt.style.use('bmh')
df1['A'].hist()
plt.savefig(PATH + 'hist3.png', dpi=300)
plt.close()

plt.style.use('dark_background')
df1['A'].hist()
plt.savefig(PATH + 'hist4.png', dpi=300)
plt.close()

plt.style.use('fivethirtyeight')
df1['A'].hist()
plt.savefig(PATH + 'hist5.png', dpi=300)
plt.close()

# Let's stick with the ggplot style and actually show you how to utilize pandas built-in plotting capabilities!
plt.style.use('ggplot')

# # Plot Types
# 
# There are several plot types built-in to pandas, most of them statistical plots by nature:
# 
# * df.plot.area     
# * df.plot.barh     
# * df.plot.density  
# * df.plot.hist     
# * df.plot.line     
# * df.plot.scatter
# * df.plot.bar      
# * df.plot.box      
# * df.plot.hexbin   
# * df.plot.kde      
# * df.plot.pie
# 
# You can also just call df.plot(kind='hist') or replace that kind argument with
# any of the key terms shown in the list above (e.g. 'box','barh', etc..)
# ___

# Let's start going through them!
# 
# ## Area
df2.plot.area(alpha=0.4)
plt.savefig(PATH + 'area.png', dpi=300)
plt.close()

# ## Barplots
print(df2.head())
df2.plot.bar()
plt.savefig(PATH + 'bar.png', dpi=300)
plt.close()

df2.plot.bar(stacked=True)
plt.savefig(PATH + 'bar_stacked.png', dpi=300)
plt.close()

# ## Histograms
df1['A'].plot.hist(bins=50)
plt.savefig(PATH + 'hist_again.png', dpi=300)
plt.close()

# ## Line Plots
# will assume the index as x
df1.plot.line(y='B',figsize=(12,3),lw=1)
plt.savefig(PATH + 'line.png', dpi=300)
plt.close()

# ## Scatter Plots
df1.plot.scatter(x='A',y='B')
plt.savefig(PATH + 'scatter.png', dpi=300)
plt.close()

# You can use c to color based off another column value
# Use cmap to indicate colormap to use. 
# For all the colormaps, check out: http://matplotlib.org/users/colormaps.html
df1.plot.scatter(x='A',y='B',c='C',cmap='coolwarm')
plt.savefig(PATH + 'scatter2.png', dpi=300)
plt.close()

# Or use s to indicate size based off another column. s parameter needs to be an 
# array, not just the name of a column:
df1.plot.scatter(x='A',y='B',s=df1['C']*200)
plt.savefig(PATH + 'scatter3.png', dpi=300)
plt.close()

# ## BoxPlots
df2.plot.box() # Can also pass a by= argument for groupby
plt.savefig(PATH + 'box.png', dpi=300)
plt.close()

# ## Hexagonal Bin Plot
# 
# Useful for Bivariate Data, alternative to scatterplot:
df = pd.DataFrame(np.random.randn(1000, 2), columns=['a', 'b'])
df.plot.hexbin(x='a',y='b',gridsize=25,cmap='Oranges')
plt.savefig(PATH + 'hexagoal.png', dpi=300)
plt.close()

# ____
# ## Kernel Density Estimation plot (KDE)
df2['a'].plot.kde()
plt.savefig(PATH + 'kde.png', dpi=300)
plt.close()

df2.plot.density()
plt.savefig(PATH + 'density.png', dpi=300)
plt.close()

# That's it! Hopefully you can see why this method of plotting will be a lot 
# easier to use than full-on matplotlib, it balances ease of use with control
# over the figure. A lot of the plot calls also accept additional arguments of 
# their parent matplotlib plt. call. 
