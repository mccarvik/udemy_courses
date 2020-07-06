#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# # Style and Color
# 
# We've shown a few times how to control figure aesthetics in seaborn, but let's 
# now go over it formally:
import pdb, sys
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/data_science_py/9_data_viz_seaborn/figs2/'
tips = sns.load_dataset('tips')

# ## Styles
# 
# You can set particular styles:
sns.countplot(x='sex',data=tips)
plt.savefig(PATH + 'count_plot.png', dpi=300)
plt.close()

sns.set_style('white')
sns.countplot(x='sex',data=tips)
plt.savefig(PATH + 'count_plot_white.png', dpi=300)
plt.close()

sns.set_style('ticks')
sns.countplot(x='sex',data=tips,palette='deep')
plt.savefig(PATH + 'count_plot_ticks.png', dpi=300)
plt.close()

# ## Spine Removal
sns.countplot(x='sex',data=tips)
sns.despine()
plt.savefig(PATH + 'count_plot_nospines.png', dpi=300)
plt.close()

sns.countplot(x='sex',data=tips)
sns.despine(left=True)
plt.savefig(PATH + 'count_plot_onespine.png', dpi=300)
plt.close()

# ## Size and Aspect
# You can use matplotlib's **plt.figure(figsize=(width,height) ** to change the 
# size of most seaborn plots.
# 
# You can control the size and aspect ratio of most seaborn grid plots by passing 
# in parameters: size, and aspect. For example:
# Non Grid Plot
plt.figure(figsize=(12,3))
sns.countplot(x='sex',data=tips)
plt.savefig(PATH + 'count_plot_sex.png', dpi=300)
plt.close()

# Grid Type Plot
sns.lmplot(x='total_bill',y='tip',size=2,aspect=4,data=tips)
plt.savefig(PATH + 'lmplot_gridtype.png', dpi=300)
plt.close()

# ## Scale and Context
# 
# The set_context() allows you to override default parameters:
sns.set_context('poster',font_scale=4)
sns.countplot(x='sex',data=tips,palette='coolwarm')
plt.savefig(PATH + 'count_plot_setcontext.png', dpi=300)
plt.close()

# Check out the documentation page for more info on these topics:
# https://stanford.edu/~mwaskom/software/seaborn/tutorial/aesthetics.html

# sns.puppyplot()
plt.savefig(PATH + 'puppyplot.png', dpi=300)
plt.close()
