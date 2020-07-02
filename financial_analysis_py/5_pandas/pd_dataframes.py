#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# # DataFrames
# 
# DataFrames are the workhorse of pandas and are directly inspired by the R programming language. We can think of a DataFrame as a bunch of Series objects put together to share the same index. Let's use pandas to explore this topic!
import pdb
import pandas as pd
import numpy as np
from numpy.random import randn
np.random.seed(101)
df = pd.DataFrame(randn(5,4),index='A B C D E'.split(),columns='W X Y Z'.split())
print(df)

# ## Selection and Indexing
# 
# Let's learn the various methods to grab data from a DataFrame
print(df['W'])

# Pass a list of column names
print(df[['W','Z']])

# SQL Syntax (NOT RECOMMENDED!)
print(df.W)

# DataFrame Columns are just Series
print(type(df['W']))

# **Creating a new column:**
df['new'] = df['W'] + df['Y']
print(df)


# ** Removing Columns**
print(df.drop('new',axis=1))
# Not inplace unless specified!
print(df)
df.drop('new',axis=1,inplace=True)
print(df)

# Can also drop rows this way:
print(df.drop('E',axis=0))

# ** Selecting Rows**
print(df.loc['A'])

# Or select based off of position instead of label 
print(df.iloc[2])

# ** Selecting subset of rows and columns **
print(df.loc['B','Y'])
print(df.loc[['A','B'],['W','Y']])

# ### Conditional Selection
# 
# An important feature of pandas is conditional selection using bracket notation, very similar to numpy:
print(df)
print(df>0)
print(df[df>0])
print(df[df['W']>0])
print(df[df['W']>0]['Y'])
print(df[df['W']>0][['Y','X']])


# For two conditions you can use | and & with parenthesis:
print(df[(df['W']>0) & (df['Y'] > 1)])
print(df[(df['W']>0) | (df['Y'] > 1)])

# ## More Index Details
# 
# Let's discuss some more features of indexing, including resetting the index or setting it something else. We'll also talk about index hierarchy!
print(df)

# Reset to default 0,1...n index
print(df.reset_index())
newind = 'CA NY WY OR CO'.split()
df['States'] = newind
print(df)
print(df.set_index('States'))
print(df)
df.set_index('States',inplace=True)
print(df)

# ## Multi-Index and Index Hierarchy
# 
# Let us go over how to work with Multi-Index, first we'll create a quick example of what a Multi-Indexed DataFrame would look like:
# Index Levels
outside = ['G1','G1','G1','G2','G2','G2']
inside = [1,2,3,1,2,3]
hier_index = list(zip(outside,inside))
hier_index = pd.MultiIndex.from_tuples(hier_index)
print(hier_index)
df = pd.DataFrame(np.random.randn(6,2),index=hier_index,columns=['A','B'])
print(df)

# Now let's show how to index this! For index hierarchy we use df.loc[], if this was on the columns axis, you would just use normal bracket notation df[]. Calling one level of the index returns the sub-dataframe:
print(df.loc['G1'])
print(df.loc['G1'].loc[1])
print(df.index.names)
df.index.names = ['Group','Num']
print(df)
print(df.loc['G1'].loc[2]['B'])

# cross section
print(df)
print(df.xs('G1'))
print(df.xs(['G1',1]))
print(df.xs(1,level='Num'))
