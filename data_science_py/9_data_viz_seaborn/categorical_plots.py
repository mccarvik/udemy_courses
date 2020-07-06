#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# # Categorical Data Plots
# 
# Now let's discuss using seaborn to plot categorical data! There are a few main plot types for this:
# 
# * factorplot
# * boxplot
# * violinplot
# * stripplot
# * swarmplot
# * barplot
# * countplot
# 
# Let's go through examples of each!
import pdb, sys
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/data_science_py/9_data_viz_seaborn/figs/'
tips = sns.load_dataset('tips')
print(tips.head())

# ## barplot and countplot
# 
# These very similar plots allow you to get aggregate data off a categorical 
# feature in your data. **barplot** is a general plot that allows you to 
# aggregate the categorical data based off some function, by default the mean:
sns.barplot(x='sex',y='total_bill',data=tips)
plt.savefig(PATH + 'barplot.png', dpi=300)
plt.close()
# You can change the estimator object to your own function, that converts a 
# vector to a scalar:
sns.barplot(x='sex',y='total_bill',data=tips,estimator=np.std)
plt.savefig(PATH + 'barplot_est.png', dpi=300)
plt.close()

# ### countplot
# 
# This is essentially the same as barplot except the estimator is explicitly 
# counting the number of occurrences. Which is why we only pass the x value:
sns.countplot(x='sex',data=tips)
plt.savefig(PATH + 'count_plot.png', dpi=300)
plt.close()

# ## boxplot and violinplot
# 
# boxplots and violinplots are used to shown the distribution of categorical
# data. A box plot (or box-and-whisker plot) shows the distribution of 
# quantitative data in a way that facilitates comparisons between variables or 
# across levels of a categorical variable. The box shows the quartiles of the 
# dataset while the whiskers extend to show the rest of the distribution, 
# except for points that are determined to be “outliers” using a method that 
# is a function of the inter-quartile range.
sns.boxplot(x="day", y="total_bill", data=tips,palette='rainbow')
plt.savefig(PATH + 'box_plot.png', dpi=300)
plt.close()

# Can do entire dataframe with orient='h'
sns.boxplot(data=tips,palette='rainbow',orient='h')
plt.savefig(PATH + 'boxplot_rainbow.png', dpi=300)
plt.close()

sns.boxplot(x="day", y="total_bill", hue="smoker",data=tips, palette="coolwarm")
plt.savefig(PATH + 'boxplot_coolwarm.png', dpi=300)
plt.close()

# ### violinplot
# A violin plot plays a similar role as a box and whisker plot. It shows the
# distribution of quantitative data across several levels of one (or more) 
# categorical variables such that those distributions can be compared. Unlike a
# box plot, in which all of the plot components correspond to actual datapoints,
# the violin plot features a kernel density estimation of the underlying 
# distribution.
sns.violinplot(x="day", y="total_bill", data=tips,palette='rainbow')
plt.savefig(PATH + 'violinplot.png', dpi=300)
plt.close()

sns.violinplot(x="day", y="total_bill", data=tips,hue='sex',palette='Set1')
plt.savefig(PATH + 'violinplot_sex.png', dpi=300)
plt.close()

sns.violinplot(x="day", y="total_bill", data=tips,hue='sex',split=True,palette='Set1')
plt.savefig(PATH + 'violinplot_split.png', dpi=300)
plt.close()

# ## stripplot and swarmplot
# The stripplot will draw a scatterplot where one variable is categorical. A 
# strip plot can be drawn on its own, but it is also a good complement to a box 
# or violin plot in cases where you want to show all observations along with 
# some representation of the underlying distribution.
# 
# The swarmplot is similar to stripplot(), but the points are adjusted (only 
# along the categorical axis) so that they don’t overlap. This gives a better 
# representation of the distribution of values, although it does not scale as 
# well to large numbers of observations (both in terms of the ability to show 
# all the points and in terms of the computation needed to arrange them).
sns.stripplot(x="day", y="total_bill", data=tips)
plt.savefig(PATH + 'strip_plot.png', dpi=300)
plt.close()

sns.stripplot(x="day", y="total_bill", data=tips,jitter=True)
plt.savefig(PATH + 'strip_plot_jitter.png', dpi=300)
plt.close()

sns.stripplot(x="day", y="total_bill", data=tips,jitter=True,hue='sex',palette='Set1')
plt.savefig(PATH + 'strip_plot_palette.png', dpi=300)
plt.close()

sns.stripplot(x="day", y="total_bill", data=tips,jitter=True,hue='sex',palette='Set1',split=True)
plt.savefig(PATH + 'strip_plot_hue.png', dpi=300)
plt.close()

sns.swarmplot(x="day", y="total_bill", data=tips)
plt.savefig(PATH + 'swarm_plot.png', dpi=300)
plt.close()

sns.swarmplot(x="day", y="total_bill",hue='sex',data=tips, palette="Set1", split=True)
plt.savefig(PATH + 'swarm_plot_palette.png', dpi=300)
plt.close()

# ### Combining Categorical Plots
sns.violinplot(x="tip", y="day", data=tips,palette='rainbow')
sns.swarmplot(x="tip", y="day", data=tips,color='black',size=3)
plt.savefig(PATH + 'swarm_violin_plot.png', dpi=300)
plt.close()

# ## factorplot
# 
# factorplot is the most general form of a categorical plot. It can take in a 
# **kind** parameter to adjust the plot type:
sns.factorplot(x='sex',y='total_bill',data=tips,kind='bar')
plt.savefig(PATH + 'factor_plot.png', dpi=300)
plt.close()
