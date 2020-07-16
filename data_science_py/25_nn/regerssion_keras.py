#!/usr/bin/env python
# coding: utf-8

# <a href="https://www.pieriandata.com"><img src="../Pierian_Data_Logo.PNG"></a>
# <strong><center>Copyright by Pierian Data Inc.</center></strong> 
# <strong><center>Created by Jose Marcial Portilla.</center></strong>

# # Keras Regression Code Along Project 
# 
# Let's now apply our knowledge to a more realistic data set. Here we will also focus 
# on feature engineering and cleaning our data!

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
# * grade - An index from 1 to 13, where 1-3 falls short of building construction and design, 
# 7 has an average level of construction and design, and 11-13 have a high quality level 
# of construction and design.
# * sqft_above - The square footage of the interior housing space that is above ground level
# * sqft_basement - The square footage of the interior housing space that is below ground level
# * yr_built - The year the house was initially built
# * yr_renovated - The year of the house’s last renovation
# * zipcode - What zipcode area the house is in
# * lat - Lattitude
# * long - Longitude
# * sqft_living15 - The square footage of interior housing living space for the nearest 15 neighbors
# * sqft_lot15 - The square footage of the land lots of the nearest 15 neighbors
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
PATH = '/home/ec2-user/environment/udemy_courses/data_science_py/25_nn/figs/'
df = pd.read_csv('../data/kc_house_data.csv')

# # Exploratory Data Analysis
print(df.isnull().sum())
print(df.describe().transpose())
plt.figure(figsize=(12,8))
sns.distplot(df['price'])
plt.savefig(PATH + 'price.png', dpi=300)
plt.close()

sns.countplot(df['bedrooms'])
plt.savefig(PATH + 'bedrooms.png', dpi=300)
plt.close()

plt.figure(figsize=(12,8))
sns.scatterplot(x='price',y='sqft_living',data=df)
plt.savefig(PATH + 'sqft.png', dpi=300)
plt.close()

sns.boxplot(x='bedrooms',y='price',data=df)
plt.savefig(PATH + 'bed_px.png', dpi=300)
plt.close()

# ### Geographical Properties
plt.figure(figsize=(12,8))
sns.scatterplot(x='price',y='long',data=df)
plt.savefig(PATH + 'price_long.png', dpi=300)
plt.close()

plt.figure(figsize=(12,8))
sns.scatterplot(x='price',y='lat',data=df)
plt.savefig(PATH + 'price_lat.png', dpi=300)
plt.close()

plt.figure(figsize=(12,8))
sns.scatterplot(x='long',y='lat',data=df,hue='price')
plt.savefig(PATH + 'long_lat.png', dpi=300)
plt.close()

print(df.sort_values('price',ascending=False).head(20))
print(len(df)*(0.01))
non_top_1_perc = df.sort_values('price',ascending=False).iloc[216:]

plt.figure(figsize=(12,8))
sns.scatterplot(x='long',y='lat',
                data=non_top_1_perc,hue='price',
                palette='RdYlGn',edgecolor=None,alpha=0.2)
plt.savefig(PATH + 'non_1_perc.png', dpi=300)
plt.close()

# ### Other Features
sns.boxplot(x='waterfront',y='price',data=df)
plt.savefig(PATH + 'waterfront.png', dpi=300)
plt.close()

# ## Working with Feature Data
print(df.head())
print(df.info())
df = df.drop('id',axis=1)
print(df.head())

# ### Feature Engineering from Date
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].apply(lambda date:date.month)
df['year'] = df['date'].apply(lambda date:date.year)
sns.boxplot(x='year',y='price',data=df)
plt.savefig(PATH + 'year.png', dpi=300)
plt.close()

sns.boxplot(x='month',y='price',data=df)
plt.savefig(PATH + 'month_px.png', dpi=300)
plt.close()

df.groupby('month').mean()['price'].plot()
plt.savefig(PATH + 'month_group.png', dpi=300)
plt.close()

df.groupby('year').mean()['price'].plot()
plt.savefig(PATH + 'year_px.png', dpi=300)
plt.close()

df = df.drop('date',axis=1)
print(df.columns)

# https://i.pinimg.com/originals/4a/ab/31/4aab31ce95d5b8474fd2cc063f334178.jpg
# May be worth considering to remove this or feature engineer categories from it
print(df['zipcode'].value_counts())
df = df.drop('zipcode',axis=1)
print(df.head())

# could make sense due to scaling, higher should correlate to more value
print(df['yr_renovated'].value_counts())
print(df['sqft_basement'].value_counts())

# ## Scaling and Train Test Split
X = df.drop('price',axis=1)
y = df['price']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=101)

# ### Scaling
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_train= scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
print(X_train.shape)
print(X_test.shape)

# ## Creating a Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam
model = Sequential()

model.add(Dense(19,activation='relu'))
model.add(Dense(19,activation='relu'))
model.add(Dense(19,activation='relu'))
model.add(Dense(19,activation='relu'))
model.add(Dense(1))

model.compile(optimizer='adam',loss='mse')

# ## Training the Model
model.fit(x=X_train,y=y_train.values,
          validation_data=(X_test,y_test.values),
          batch_size=128,epochs=400)

losses = pd.DataFrame(model.history.history)
losses.plot()
plt.savefig(PATH + 'losses.png', dpi=300)
plt.close()

# # Evaluation on Test Data
# 
# https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics
from sklearn.metrics import mean_squared_error,mean_absolute_error,explained_variance_score

# #### Predicting on Brand New Data
print(X_test)
predictions = model.predict(X_test)
print(mean_absolute_error(y_test,predictions))
print(np.sqrt(mean_squared_error(y_test,predictions)))
print(explained_variance_score(y_test,predictions))

print(df['price'].mean())
print(df['price'].median())

# Our predictions
plt.scatter(y_test,predictions)
plt.savefig(PATH + 'y_preds.png', dpi=300)
plt.close()

# Perfect predictions
plt.plot(y_test,y_test,'r')
plt.savefig(PATH + 'perf_preds.png', dpi=300)
plt.close()

errors = y_test.values.reshape(6480, 1) - predictions
sns.distplot(errors)
plt.savefig(PATH + 'errors.png', dpi=300)
plt.close()

# -------------
# ### Predicting on a brand new house
single_house = df.drop('price',axis=1).iloc[0]
single_house = scaler.transform(single_house.values.reshape(-1, 19))
print(single_house)

model.predict(single_house)
print(df.iloc[0])
