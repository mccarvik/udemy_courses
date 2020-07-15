#!/usr/bin/env python
# coding: utf-8

# <a href="https://www.pieriandata.com"><img src="../Pierian_Data_Logo.PNG"></a>
# <strong><center>Copyright by Pierian Data Inc.</center></strong> 
# <strong><center>Created by Jose Marcial Portilla.</center></strong>

# # Keras Regression Code Along Project 
# 
# Let's now apply our knowledge to a more realistic data set. Here we will also focus on feature engineering and cleaning our data!

# ## The Data
# 
# We will be using data from a Kaggle data set:
# 
# https://www.kaggle.com/harlfoxem/housesalesprediction
# 
# #### Feature Columns
#     
# * id - Unique ID for each home sold
# * date - Date of the home sale
# * price - Price of each home sold
# * bedrooms - Number of bedrooms
# * bathrooms - Number of bathrooms, where .5 accounts for a room with a toilet but no shower
# * sqft_living - Square footage of the apartments interior living space
# * sqft_lot - Square footage of the land space
# * floors - Number of floors
# * waterfront - A dummy variable for whether the apartment was overlooking the waterfront or not
# * view - An index from 0 to 4 of how good the view of the property was
# * condition - An index from 1 to 5 on the condition of the apartment,
# * grade - An index from 1 to 13, where 1-3 falls short of building construction and design, 7 has an average level of construction and design, and 11-13 have a high quality level of construction and design.
# * sqft_above - The square footage of the interior housing space that is above ground level
# * sqft_basement - The square footage of the interior housing space that is below ground level
# * yr_built - The year the house was initially built
# * yr_renovated - The year of the house’s last renovation
# * zipcode - What zipcode area the house is in
# * lat - Lattitude
# * long - Longitude
# * sqft_living15 - The square footage of interior housing living space for the nearest 15 neighbors
# * sqft_lot15 - The square footage of the land lots of the nearest 15 neighbors

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df = pd.read_csv('../data/kc_house_data.csv')


# # Exploratory Data Analysis

# In[3]:


df.isnull().sum()


# In[4]:


df.describe().transpose()


# In[5]:


plt.figure(figsize=(12,8))
sns.distplot(df['price'])


# In[6]:


sns.countplot(df['bedrooms'])


# In[7]:


plt.figure(figsize=(12,8))
sns.scatterplot(x='price',y='sqft_living',data=df)


# In[8]:


sns.boxplot(x='bedrooms',y='price',data=df)


# ### Geographical Properties

# In[9]:


plt.figure(figsize=(12,8))
sns.scatterplot(x='price',y='long',data=df)


# In[10]:


plt.figure(figsize=(12,8))
sns.scatterplot(x='price',y='lat',data=df)


# In[11]:


plt.figure(figsize=(12,8))
sns.scatterplot(x='long',y='lat',data=df,hue='price')


# In[12]:


df.sort_values('price',ascending=False).head(20)


# In[13]:


len(df)*(0.01)


# In[14]:


non_top_1_perc = df.sort_values('price',ascending=False).iloc[216:]


# In[15]:


plt.figure(figsize=(12,8))
sns.scatterplot(x='long',y='lat',
                data=non_top_1_perc,hue='price',
                palette='RdYlGn',edgecolor=None,alpha=0.2)


# ### Other Features

# In[16]:


sns.boxplot(x='waterfront',y='price',data=df)


# ## Working with Feature Data

# In[17]:


df.head()


# In[18]:


df.info()


# In[19]:


df = df.drop('id',axis=1)


# In[20]:


df.head()


# ### Feature Engineering from Date

# In[21]:


df['date'] = pd.to_datetime(df['date'])


# In[22]:


df['month'] = df['date'].apply(lambda date:date.month)


# In[23]:


df['year'] = df['date'].apply(lambda date:date.year)


# In[24]:


sns.boxplot(x='year',y='price',data=df)


# In[25]:


sns.boxplot(x='month',y='price',data=df)


# In[26]:


df.groupby('month').mean()['price'].plot()


# In[27]:


df.groupby('year').mean()['price'].plot()


# In[28]:


df = df.drop('date',axis=1)


# In[29]:


df.columns


# In[30]:


# https://i.pinimg.com/originals/4a/ab/31/4aab31ce95d5b8474fd2cc063f334178.jpg
# May be worth considering to remove this or feature engineer categories from it
df['zipcode'].value_counts()


# In[31]:


df = df.drop('zipcode',axis=1)


# In[32]:


df.head()


# In[33]:


# could make sense due to scaling, higher should correlate to more value
df['yr_renovated'].value_counts()


# In[34]:


df['sqft_basement'].value_counts()


# ## Scaling and Train Test Split

# In[35]:


X = df.drop('price',axis=1)
y = df['price']


# In[36]:


from sklearn.model_selection import train_test_split


# In[37]:


X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=101)


# ### Scaling

# In[38]:


from sklearn.preprocessing import MinMaxScaler


# In[39]:


scaler = MinMaxScaler()


# In[40]:


X_train= scaler.fit_transform(X_train)


# In[41]:


X_test = scaler.transform(X_test)


# In[42]:


X_train.shape


# In[43]:


X_test.shape


# ## Creating a Model

# In[44]:


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam


# In[45]:


model = Sequential()

model.add(Dense(19,activation='relu'))
model.add(Dense(19,activation='relu'))
model.add(Dense(19,activation='relu'))
model.add(Dense(19,activation='relu'))
model.add(Dense(1))

model.compile(optimizer='adam',loss='mse')


# ## Training the Model

# In[46]:


model.fit(x=X_train,y=y_train.values,
          validation_data=(X_test,y_test.values),
          batch_size=128,epochs=400)


# In[47]:


losses = pd.DataFrame(model.history.history)


# In[48]:


losses.plot()


# # Evaluation on Test Data
# 
# https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics

# In[49]:


from sklearn.metrics import mean_squared_error,mean_absolute_error,explained_variance_score


# #### Predicting on Brand New Data

# In[50]:


X_test


# In[51]:


predictions = model.predict(X_test)


# In[52]:


mean_absolute_error(y_test,predictions)


# In[53]:


np.sqrt(mean_squared_error(y_test,predictions))


# In[54]:


explained_variance_score(y_test,predictions)


# In[55]:


df['price'].mean()


# In[56]:


df['price'].median()


# In[57]:


# Our predictions
plt.scatter(y_test,predictions)

# Perfect predictions
plt.plot(y_test,y_test,'r')


# In[58]:


errors = y_test.values.reshape(6480, 1) - predictions


# In[59]:


sns.distplot(errors)


# -------------
# ### Predicting on a brand new house

# In[81]:


single_house = df.drop('price',axis=1).iloc[0]


# In[86]:


single_house = scaler.transform(single_house.values.reshape(-1, 19))


# In[87]:


single_house


# In[89]:


model.predict(single_house)


# In[90]:


df.iloc[0]

