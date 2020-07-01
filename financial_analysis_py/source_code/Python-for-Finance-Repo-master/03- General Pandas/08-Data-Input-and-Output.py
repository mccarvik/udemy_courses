#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# ** Typically we will just be either reading csv files directly or using pandas-datareader or quandl. Consider this lecture just a quick overview of what is possible with pandas (we won't be working with SQL or excel files in this course) **

# # Data Input and Output
# 
# This notebook is the reference code for getting input and output, pandas can read a variety of file types using its pd.read_ methods. Let's take a look at the most common data types:

# In[1]:


import numpy as np
import pandas as pd


# ## CSV
# 
# ### CSV Input

# In[25]:


df = pd.read_csv('example')
df


# ### CSV Output

# In[24]:


df.to_csv('example',index=False)


# ## Excel
# Pandas can read and write excel files, keep in mind, this only imports data. Not formulas or images, having images or macros may cause this read_excel method to crash. 

# ### Excel Input

# In[35]:


pd.read_excel('Excel_Sample.xlsx',sheetname='Sheet1')


# ### Excel Output

# In[33]:


df.to_excel('Excel_Sample.xlsx',sheet_name='Sheet1')


# ## HTML
# 
# You may need to install htmllib5,lxml, and BeautifulSoup4. In your terminal/command prompt run:
# 
#     conda install lxml
#     conda install html5lib
#     conda install BeautifulSoup4
# 
# Then restart Jupyter Notebook.
# (or use pip install if you aren't using the Anaconda Distribution)
# 
# Pandas can read table tabs off of html. For example:

# ### HTML Input
# 
# Pandas read_html function will read tables off of a webpage and return a list of DataFrame objects:

# In[5]:


df = pd.read_html('http://www.fdic.gov/bank/individual/failed/banklist.html')


# In[7]:


df[0]


# ____

# # Great Job!
