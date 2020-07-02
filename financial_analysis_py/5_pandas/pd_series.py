#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___
# # Series

# The first main data type we will learn about for pandas is the Series data type. Let's import Pandas and explore the Series object.
# 
# A Series is very similar to a NumPy array (in fact it is built on top of the NumPy array object). What differentiates the NumPy array from a Series, is that a Series can have axis labels, meaning it can be indexed by a label, instead of just a number location. It also doesn't need to hold numeric data, it can hold any arbitrary Python Object.
# 
# Let's explore this concept through some examples:
import numpy as np
import pandas as pd

# ### Creating a Series
# 
# You can convert a list,numpy array, or dictionary to a Series:
labels = ['a','b','c']
my_list = [10,20,30]
arr = np.array([10,20,30])
d = {'a':10,'b':20,'c':30}

# ** Using Lists**
print(pd.Series(data=my_list))
print(pd.Series(data=my_list,index=labels))
print(pd.Series(my_list,labels))

# ** NumPy Arrays **
print(pd.Series(arr))
print(pd.Series(arr,labels))


# ** Dictionary**
print(pd.Series(d))

# ### Data in a Series
# 
# A pandas Series can hold a variety of object types:
print(pd.Series(data=labels))

# Even functions (although unlikely that you will use this)
print(pd.Series([sum,print,len]))

# ## Using an Index
# 
# The key to using a Series is understanding its index. Pandas makes use of these index names or numbers by allowing for fast look ups of information (works like a hash table or dictionary).
# 
# Let's see some examples of how to grab information from a Series. Let us create two sereis, ser1 and ser2:
ser1 = pd.Series([1,2,3,4],index = ['USA', 'Germany','USSR', 'Japan'])                                   
print(ser1)
ser2 = pd.Series([1,2,5,4],index = ['USA', 'Germany','Italy', 'Japan'])                                   
print(ser2)
print(ser1['USA'])

# Operations are then also done based off of index:
print(ser1 + ser2)
