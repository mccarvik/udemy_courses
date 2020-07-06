#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# # Matrix Plots
# 
# Matrix plots allow you to plot data as color-encoded matrices and can also be
# used to indicate clusters within the data (later in the machine learning 
# section we will learn how to formally cluster data).
# 
# Let's begin by exploring seaborn's heatmap and clutermap:
import pdb, sys
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/data_science_py/9_data_viz_seaborn/figs/'

flights = sns.load_dataset('flights')
tips = sns.load_dataset('tips')
print(tips.head())
print(flights.head())


# ## Heatmap
# 
# In order for a heatmap to work properly, your data should already be in a 
# matrix form, the sns.heatmap function basically just colors it in for you. 
# For example:
print(tips.head())

# Matrix form for correlation data
print(tips.corr())

sns.heatmap(tips.corr())
plt.savefig(PATH + 'heatmap.png', dpi=300)
plt.close()

sns.heatmap(tips.corr(),cmap='coolwarm',annot=True)
plt.savefig(PATH + 'heatmap_coolwarm.png', dpi=300)
plt.close()

# Or for the flights data:
print(flights.pivot_table(values='passengers',index='month',columns='year'))

pvflights = flights.pivot_table(values='passengers',index='month',columns='year')
sns.heatmap(pvflights)
plt.savefig(PATH + 'pt_heatmap.png', dpi=300)
plt.close()

sns.heatmap(pvflights,cmap='magma',linecolor='white',linewidths=1)
plt.savefig(PATH + 'pt_magma_heatmap.png', dpi=300)
plt.close()

# ## clustermap
# 
# The clustermap uses hierarchal clustering to produce a clustered version of 
# the heatmap. For example:
sns.clustermap(pvflights)
plt.savefig(PATH + 'clustermap.png', dpi=300)
plt.close()

# Notice now how the years and months are no longer in order, instead they are 
# grouped by similarity in value (passenger count). That means we can begin to 
# infer things from this plot, such as August and July being similar (makes sense,
# since they are both summer travel months)
# More options to get the information a little clearer like normalization
sns.clustermap(pvflights,cmap='coolwarm',standard_scale=1)
plt.savefig(PATH + 'clustermap_coolwarm.png', dpi=300)
plt.close()
