#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# # Groupby
# 
# The groupby method allows you to group rows of data together and call aggregate functions

import pandas as pd
# Create dataframe
data = {'Company':['GOOG','GOOG','MSFT','MSFT','FB','FB'],
       'Person':['Sam','Charlie','Amy','Vanessa','Carl','Sarah'],
       'Sales':[200,120,340,124,243,350]}

df = pd.DataFrame(data)
print(df)

# ** Now you can use the .groupby() method to group rows together based off of a column name. For instance let's group based off of Company. This will create a DataFrameGroupBy object:**
print(df.groupby('Company'))

# You can save this object as a new variable:
by_comp = df.groupby("Company")

# And then call aggregate methods off the object:
print(by_comp.mean())
print(df.groupby('Company').mean())

# More examples of aggregate methods:
print(by_comp.std())
print(by_comp.min())
print(by_comp.max())
print(by_comp.count())
print(by_comp.describe())
print(by_comp.describe().transpose())
print(by_comp.describe().transpose()['GOOG'])
