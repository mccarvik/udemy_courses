#!/usr/bin/env python
# coding: utf-8

# <a href="https://www.pieriandata.com"><img src="../Pierian_Data_Logo.PNG"></a>
# <strong><center>Copyright by Pierian Data Inc.</center></strong> 
# <strong><center>Created by Jose Marcial Portilla.</center></strong>

# # Tensorboard
# 
# ---
# ---
# 
# **NOTE: You must watch the corresponding video to understand this lecture. This notebook can't serve as a full guide. Please watch the video BEFORE posting questions to the QA forum.**
# 
# ---
# ---
# 
# Let's explore the built in data visualization capabilities that come with Tensorboard.
# 
# Full official tutorial available here: https://www.tensorflow.org/tensorboard/get_started
# 
# ## Data

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


df = pd.read_csv('../DATA/cancer_classification.csv')


# ### Train Test Split

# In[3]:


X = df.drop('benign_0__mal_1',axis=1).values
y = df['benign_0__mal_1'].values


# In[4]:


from sklearn.model_selection import train_test_split


# In[5]:


X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state=101)


# 
# ### Scaling Data

# In[6]:


from sklearn.preprocessing import MinMaxScaler


# In[7]:


scaler = MinMaxScaler()


# In[8]:


scaler.fit(X_train)


# In[9]:


X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


# ## Creating the Model

# In[10]:


import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation,Dropout


# In[11]:


from tensorflow.keras.callbacks import EarlyStopping,TensorBoard


# In[12]:


early_stop = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=25)


# In[13]:


pwd


# ## Creating the Tensorboard Callback
# 
# TensorBoard is a visualization tool provided with TensorFlow.
# 
# This callback logs events for TensorBoard, including:
# * Metrics summary plots
# * Training graph visualization
# * Activation histograms
# * Sampled profiling
# 
# If you have installed TensorFlow with pip, you should be able
# to launch TensorBoard from the command line:
# 
# ```sh
# tensorboard --logdir=path_to_your_logs
# ```
# 
# You can find more information about TensorBoard
# [here](https://www.tensorflow.org/tensorboard/).
# 
#     Arguments:
#         log_dir: the path of the directory where to save the log files to be
#           parsed by TensorBoard.
#         histogram_freq: frequency (in epochs) at which to compute activation and
#           weight histograms for the layers of the model. If set to 0, histograms
#           won't be computed. Validation data (or split) must be specified for
#           histogram visualizations.
#         write_graph: whether to visualize the graph in TensorBoard. The log file
#           can become quite large when write_graph is set to True.
#         write_images: whether to write model weights to visualize as image in
#           TensorBoard.
#         update_freq: `'batch'` or `'epoch'` or integer. When using `'batch'`,
#           writes the losses and metrics to TensorBoard after each batch. The same
#           applies for `'epoch'`. If using an integer, let's say `1000`, the
#           callback will write the metrics and losses to TensorBoard every 1000
#           samples. Note that writing too frequently to TensorBoard can slow down
#           your training.
#         profile_batch: Profile the batch to sample compute characteristics. By
#           default, it will profile the second batch. Set profile_batch=0 to
#           disable profiling. Must run in TensorFlow eager mode.
#         embeddings_freq: frequency (in epochs) at which embedding layers will
#           be visualized. If set to 0, embeddings won't be visualized.
#        

# In[14]:


from datetime import datetime


# In[15]:


datetime.now().strftime("%Y-%m-%d--%H%M")


# In[16]:


# WINDOWS: Use "logs\\fit"
# MACOS/LINUX: Use "logs\fit"

log_directory = 'logs\\fit'

# OPTIONAL: ADD A TIMESTAMP FOR UNIQUE FOLDER
# timestamp = datetime.now().strftime("%Y-%m-%d--%H%M")
# log_directory = log_directory + '\\' + timestamp


board = TensorBoard(log_dir=log_directory,histogram_freq=1,
    write_graph=True,
    write_images=True,
    update_freq='epoch',
    profile_batch=2,
    embeddings_freq=1)


# Now create the model layers:

# In[17]:


model = Sequential()
model.add(Dense(units=30,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=15,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=1,activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam')


# ## Train the Model

# In[18]:


model.fit(x=X_train, 
          y=y_train, 
          epochs=600,
          validation_data=(X_test, y_test), verbose=1,
          callbacks=[early_stop,board]
          )


# # Running Tensorboard
# 

# ## Running through the Command Line
# 
# **Watch video to see how to run Tensorboard through a command line call.**

# Tensorboard will run locally in your browser at [http://localhost:6006/](http://localhost:6006/)
# 

# In[19]:


print(log_directory)


# In[20]:


pwd


# ### Use cd at your command line to change directory to the file path reported back by pwd or your current .py file location.
# ### Then run this code at your command line or terminal

# In[ ]:


tensorboard --logdir logs\fit 

