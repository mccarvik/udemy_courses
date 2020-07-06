#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# # Grids
# 
# Grids are general types of plots that allow you to map plot types to rows 
# and columns of a grid, this helps you create similar plots separated by features.
import pdb, sys
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/data_science_py/9_data_viz_seaborn/figs/'
iris = sns.load_dataset('iris')
print(iris.head())

# ## PairGrid
# 
# Pairgrid is a subplot grid for plotting pairwise relationships in a dataset.
# Just the Grid
sns.PairGrid(iris)
plt.savefig(PATH + 'pairgrid1.png', dpi=300)
plt.close()

# Then you map to the grid
g = sns.PairGrid(iris)
g.map(plt.scatter)
plt.savefig(PATH + 'pairgrid2.png', dpi=300)
plt.close()


# Map to upper,lower, and diagonal
g = sns.PairGrid(iris)
g.map_diag(plt.hist)
g.map_upper(plt.scatter)
g.map_lower(sns.kdeplot)
plt.savefig(PATH + 'pairgrid3.png', dpi=300)
plt.close()

# ## pairplot
# 
# pairplot is a simpler version of PairGrid (you'll use quite often)
sns.pairplot(iris)
sns.pairplot(iris,hue='species',palette='rainbow')
plt.savefig(PATH + 'pairplot1.png', dpi=300)
plt.close()


# ## Facet Grid
# 
# FacetGrid is the general way to create grids of plots based off of a feature:
tips = sns.load_dataset('tips')
print(tips.head())

# Just the Grid
g = sns.FacetGrid(tips, col="time", row="smoker")
plt.savefig(PATH + 'facet_grid.png', dpi=300)
plt.close()

g = sns.FacetGrid(tips, col="time",  row="smoker")
g = g.map(plt.hist, "total_bill")
plt.savefig(PATH + 'facet_grid_smoker.png', dpi=300)
plt.close()


g = sns.FacetGrid(tips, col="time",  row="smoker",hue='sex')
# Notice hwo the arguments come after plt.scatter call
g = g.map(plt.scatter, "total_bill", "tip").add_legend()
plt.savefig(PATH + 'facet_grid_hue.png', dpi=300)
plt.close()


# ## JointGrid
# 
# JointGrid is the general version for jointplot() type grids, for a quick example:
g = sns.JointGrid(x="total_bill", y="tip", data=tips)
plt.savefig(PATH + 'joint_grid.png', dpi=300)
plt.close()


g = sns.JointGrid(x="total_bill", y="tip", data=tips)
g = g.plot(sns.regplot, sns.distplot)
plt.savefig(PATH + 'joint_grid_tips.png', dpi=300)
plt.close()
# Reference the documentation as necessary for grid types, but most of the time
# you'll just use the easier plots discussed earlier.
# # Great Job!
