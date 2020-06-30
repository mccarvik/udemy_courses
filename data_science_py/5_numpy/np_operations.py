#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# # NumPy Operations

# ## Arithmetic
# 
# You can easily perform array with array arithmetic, or scalar with array arithmetic. Let's see some examples:

import numpy as np
arr = np.arange(0,10)
print(arr + arr)
print(arr * arr)
print(arr - arr)

# Warning on division by zero, but not an error!
# Just replaced with nan
print(arr/arr)

# Also warning, but not an error instead infinity
print(1/arr)
print(arr**3)

# ## Universal Array Functions
# 
# Numpy comes with many [universal array functions](http://docs.scipy.org/doc/numpy/reference/ufuncs.html), which are essentially just mathematical operations you can use to perform the operation across the array. Let's show some common ones:
#Taking Square Roots
print(np.sqrt(arr))

#Calcualting exponential (e^)
print(np.exp(arr))

print(np.max(arr)) #same as arr.max()
print(np.sin(arr))
print(np.log(arr))
