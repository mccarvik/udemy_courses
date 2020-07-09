#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___
# # Plotly and Cufflinks

# Plotly is a library that allows you to create interactive plots that you can use in 
# dashboards or websites (you can save them as html files or static images).
# 
# ## Installation
# 
# In order for this all to work, you'll need to install plotly and cufflinks to call plots 
# directly off of a pandas dataframe. These libraries are not currently available through 
# **conda** but are available through **pip**. Install the libraries at your command 
# line/terminal using:
# 
#     pip install plotly
#     pip install cufflinks
# 
# ** NOTE: Make sure you only have one installation of Python on your computer when you 
# do this, otherwise the installation may not work. **
# 
# ## Imports and Set-up
import pdb, sys
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/data_science_py/11_plotly/figs/'
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# print(__version__) # requires version >= 1.9.0
import cufflinks as cf

# For Notebooks
# init_notebook_mode(connected=True)

# For offline use
cf.go_offline()


# NOTE!!!!!!!!
# All these charts are for intereactive use on a web browser and will freeze
# when ran from a command line


# ### Fake Data
df = pd.DataFrame(np.random.randn(100,4),columns='A B C D'.split())
print(df.head())

df2 = pd.DataFrame({'Category':['A','B','C'],'Values':[32,43,50]})
print(df2.head())

# ## Using Cufflinks and iplot()
# 
# * scatter
# * bar
# * box
# * spread
# * ratio
# * heatmap
# * surface
# * histogram
# * bubble

# ## Scatter
df.iplot(kind='scatter',x='A',y='B',mode='markers',size=10)

# ## Bar Plots
df2.iplot(kind='bar',x='Category',y='Values')

df.count().iplot(kind='bar')

# ## Boxplots
df.iplot(kind='box')

# ## 3d Surface
df3 = pd.DataFrame({'x':[1,2,3,4,5],'y':[10,20,30,20,10],'z':[5,4,3,2,1]})

df3.iplot(kind='surface',colorscale='rdylbu')

# ## Spread
df[['A','B']].iplot(kind='spread')

# ## histogram
df['A'].iplot(kind='hist',bins=25)

df.iplot(kind='bubble',x='A',y='B',size='C')

# ## scatter_matrix()
# 
# Similar to sns.pairplot()
df.scatter_matrix()
