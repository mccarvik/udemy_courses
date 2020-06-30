#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# # NumPy 
# 
# NumPy (or Numpy) is a Linear Algebra Library for Python, the reason it is so important for Data Science with Python is that almost all of the libraries in the PyData Ecosystem rely on NumPy as one of their main building blocks.
# 
# Numpy is also incredibly fast, as it has bindings to C libraries. For more info on why you would want to use Arrays instead of lists, check out this great [StackOverflow post](http://stackoverflow.com/questions/993984/why-numpy-instead-of-python-lists).
# 
# We will only learn the basics of NumPy, to get started we need to install it!

# ## Installation Instructions
# 
# **It is highly recommended you install Python using the Anaconda distribution to make sure all underlying dependencies (such as Linear Algebra libraries) all sync up with the use of a conda install. If you have Anaconda, install NumPy by going to your terminal or command prompt and typing:**
#     
#     conda install numpy
#     
# **If you do not have Anaconda and can not install it, please refer to [Numpy's official documentation on various installation instructions.](http://docs.scipy.org/doc/numpy-1.10.1/user/install.html)**

# ## Using NumPy
# 
# Once you've installed NumPy you can import it as a library:

# In[1]:


import numpy as np


# Numpy has many built-in functions and capabilities. We won't cover them all but instead we will focus on some of the most important aspects of Numpy: vectors,arrays,matrices, and number generation. Let's start by discussing arrays.
# 
# # Numpy Arrays
# 
# NumPy arrays are the main way we will use Numpy throughout the course. Numpy arrays essentially come in two flavors: vectors and matrices. Vectors are strictly 1-d arrays and matrices are 2-d (but you should note a matrix can still have only one row or one column).
# 
# Let's begin our introduction by exploring how to create NumPy arrays.
# 
# ## Creating NumPy Arrays
# 
# ### From a Python List
# 
# We can create an array by directly converting a list or list of lists:

# In[19]:


my_list = [1,2,3]
print(my_list)
print(np.array(my_list))
my_matrix = [[1,2,3],[4,5,6],[7,8,9]]
print(my_matrix)
print(np.array(my_matrix))

# ## Built-in Methods
# 
# There are lots of built-in ways to generate Arrays

# ### arange
# 
# Return evenly spaced values within a given interval.
print(np.arange(0,10))
print(np.arange(0,11,2))

# ### zeros and ones
# 
# Generate arrays of zeros or ones
print(np.zeros(3))
print(np.zeros((5,5)))
print(np.ones(3))
print(np.ones((3,3)))

# ### linspace
# Return evenly spaced numbers over a specified interval.
print(np.linspace(0,10,3))
print(np.linspace(0,10,50))

# ## eye
# 
# Creates an identity matrix
print(np.eye(4))

# ## Random 
# 
# Numpy also has lots of ways to create random number arrays:
# 
# ### rand
# Create an array of the given shape and populate it with
# random samples from a uniform distribution
# over ``[0, 1)``.
print(np.random.rand(2))
# for 2 dimensionl array:
print(np.random.rand(5,5))

# ### randn
# 
# Return a sample (or samples) from the "standard normal" distribution. Unlike rand which is uniform:
print(np.random.randn(2))
# for 2 dimensionl array:
print(np.random.randn(5,5))

# ### randint
# Return random integers from `low` (inclusive) to `high` (exclusive).
print(np.random.randint(1,100))
# will give 10 integers
print(np.random.randint(1,100,10))

# ## Array Attributes and Methods
# 
# Let's discuss some useful attributes and methods or an array:
arr = np.arange(25)
ranarr = np.random.randint(0,50,10)
print(arr)
print(ranarr)

# ## Reshape
# Returns an array containing the same data with a new shape.
# rows * cols must equal number of elements in the array
print(arr.reshape(5,5))

# ### max,min,argmax,argmin
# 
# These are useful methods for finding max or min values. Or to find their index locations using argmin or argmax
# argmax and argmin return the index of the max and min vals
print(ranarr)
print(ranarr.max())
print(ranarr.argmax())
print(ranarr.min())
print(ranarr.argmin())

# ## Shape
# 
# Shape is an attribute that arrays have (not a method):

# Vector
print(arr.shape)

# Notice the two sets of brackets
print(arr.reshape(1,25))
print(arr.reshape(1,25).shape)
print(arr.reshape(25,1))
print(arr.reshape(25,1).shape)

# ### dtype
# 
# You can also grab the data type of the object in the array:
print(arr.dtype)
