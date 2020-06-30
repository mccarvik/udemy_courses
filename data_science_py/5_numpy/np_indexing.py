#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# # NumPy Indexing and Selection
# 
# In this lecture we will discuss how to select elements or groups of elements from an array.

import numpy as np
#Creating sample array
arr = np.arange(0,11)
#Show
print(arr)

# ## Bracket Indexing and Selection
# The simplest way to pick one or some elements of an array looks very similar to python lists:
#Get a value at an index
print(arr[8])

#Get values in a range
print(arr[1:5])

#Get values in a range
print(arr[:5])

# ## Broadcasting
# 
# Numpy arrays differ from a normal Python list because of their ability to broadcast:
#Setting a value with index range (Broadcasting)
arr[0:5]=100
#Show
print(arr)
# Reset array, we'll see why I had to reset in  a moment
arr = np.arange(0,11)
#Show
print(arr)

#Important notes on Slices
slice_of_arr = arr[0:6]

#Show slice
print(slice_of_arr)

#Change Slice
slice_of_arr[:]=99

#Show Slice again
print(slice_of_arr)

# Now note the changes also occur in our original array!
print(arr)

# Data is not copied, it's a view of the original array! This avoids memory problems!
#To get a copy, need to be explicit
arr_copy = arr.copy()
print(arr_copy)

# ## Indexing a 2D array (matrices)
# 
# The general format is **arr_2d[row][col]** or **arr_2d[row,col]**. I recommend usually using the comma notation for clarity.
arr_2d = np.array(([5,10,15],[20,25,30],[35,40,45]))

#Show
print(arr_2d)

#Indexing row
print(arr_2d[1])
# Format is arr_2d[row][col] or arr_2d[row,col]
# Getting individual element value
print(arr_2d[1][0])

# Getting individual element value
print(arr_2d[1,0])

# 2D array slicing
#Shape (2,2) from top right corner
print(arr_2d[:2,1:])
#Shape bottom row
print(arr_2d[2])
#Shape bottom row
print(arr_2d[2,:])

# ### Fancy Indexing
# 
# Fancy indexing allows you to select entire rows or columns out of order,to show this, let's quickly build out a numpy array:
#Set up matrix
arr2d = np.zeros((10,10))

#Length of array
arr_length = arr2d.shape[1]

#Set up array
for i in range(arr_length):
    arr2d[i] = i
print(arr2d)
# Fancy indexing allows the following
print(arr2d[[2,4,6,8]])

#Allows in any order
arr2d[[6,4,2,7]]

# ## More Indexing Help
# Indexing a 2d matrix can be a bit confusing at first, especially when you start to add in step size. Try google image searching NumPy indexing to fins useful images, like this one:
# 
# <img src= 'http://memory.osu.edu/classes/python/_images/numpy_indexing.png' width=500/>

# ## Selection
# 
# Let's briefly go over how to use brackets for selection based off of comparison operators.
arr = np.arange(1,11)
print(arr)
print(arr > 4)
bool_arr = arr>4
print(bool_arr)
print(arr[bool_arr])
print(arr[arr>2])

x = 2
print(arr[arr>x])
