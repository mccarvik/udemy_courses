#!/usr/bin/env python
# coding: utf-8

# <a href="https://www.pieriandata.com"><img src="../Pierian_Data_Logo.PNG"></a>
# <strong><center>Copyright by Pierian Data Inc.</center></strong> 
# <strong><center>Created by Jose Marcial Portilla.</center></strong>

# # Keras Syntax Basics
# 
# With TensorFlow 2.0 , Keras is now the main API choice. Let's work through a 
# simple regression project to understand the basics of the Keras syntax and adding layers.

# ## The Data
# 
# To learn the basic syntax of Keras, we will use a very simple fake data set, 
# in the subsequent lectures we will focus on real datasets, along with feature 
# engineering! For now, let's focus on the syntax of TensorFlow 2.0.
# 
# Let's pretend this data are measurements of some rare gem stones, with 2 
# measurement features and a sale price. Our final goal would be to try to predict 
# the sale price of a new gem stone we just mined from the ground, in order to try
# to set a fair price in the market.
# 
# ### Load the Data
import pandas as pd
PATH = '/home/ec2-user/environment/udemy_courses/data_science_py/25_nn/figs/'
df = pd.read_csv('DATA/fake_reg.csv')
print(df.head())

# ### Explore the data
# 
# Let's take a quick look, we should see strong correlation between the features 
# and the "price" of this made up product.
import seaborn as sns
import matplotlib.pyplot as plt
sns.pairplot(df)
plt.savefig(PATH + 'fake_reg.png', dpi=300)
plt.close()

# Feel free to visualize more, but this data is fake, so we will focus on feature
# engineering and exploratory data analysis later on in the course in much more detail!
# ### Test/Train Split
from sklearn.model_selection import train_test_split
# Convert Pandas to Numpy for Keras

# Features
X = df[['feature1','feature2']].values

# Label
y = df['price'].values

# Split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=42)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

# ## Normalizing/Scaling the Data
# 
# We scale the feature data.
# 
# [Why we don't need to scale the label](https://stats.stackexchange.com/questions/111467/is-it-necessary-to-scale-the-target-value-in-addition-to-scaling-features-for-re)
from sklearn.preprocessing import MinMaxScaler
help(MinMaxScaler)
scaler = MinMaxScaler()

# Notice to prevent data leakage from the test set, we only fit our scaler to the training set
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# # TensorFlow 2.0 Syntax
# 
# 
# ## Import Options
# 
# There are several ways you can import Keras from Tensorflow (this is hugely a
# personal style choice, please use any import methods you prefer). We will use 
# the method shown in the **official TF documentation**.
import tensorflow as tf
from tensorflow.keras.models import Sequential
help(Sequential)

# ## Creating a Model
# 
# There are two ways to create models through the TF 2 Keras API, either pass in 
# a list of layers all at once, or add them one by one.
# 
# Let's show both methods (its up to you to choose which method you prefer).
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation

# ### Model - as a list of layers
model = Sequential([
    Dense(units=2),
    Dense(units=2),
    Dense(units=2)
])

# ### Model - adding in layers one by one
model = Sequential()
model.add(Dense(2))
model.add(Dense(2))
model.add(Dense(2))

# Let's go ahead and build a simple model and then compile it by defining our solver
model = Sequential()

model.add(Dense(4,activation='relu'))
model.add(Dense(4,activation='relu'))
model.add(Dense(4,activation='relu'))

# Final output node for prediction
model.add(Dense(1))
model.compile(optimizer='rmsprop',loss='mse')

# ### Choosing an optimizer and loss
# 
# Keep in mind what kind of problem you are trying to solve:
# 
#     # For a multi-class classification problem
#     model.compile(optimizer='rmsprop',
#                   loss='categorical_crossentropy',
#                   metrics=['accuracy'])
# 
#     # For a binary classification problem
#     model.compile(optimizer='rmsprop',
#                   loss='binary_crossentropy',
#                   metrics=['accuracy'])
# 
#     # For a mean squared error regression problem
#     model.compile(optimizer='rmsprop',
#                   loss='mse')

# # Training
# 
# Below are some common definitions that are necessary to know and understand to correctly utilize Keras:
# 
# * Sample: one element of a dataset.
#     * Example: one image is a sample in a convolutional network
#     * Example: one audio file is a sample for a speech recognition model
# * Batch: a set of N samples. The samples in a batch are processed independently, in 
# parallel. If training, a batch results in only one update to the model.A batch generally
# approximates the distribution of the input data better than a single input. The larger 
# the batch, the better the approximation; however, it is also true that the batch will 
# take longer to process and will still result in only one update. For inference 
# (evaluate/predict), it is recommended to pick a batch size that is as large as 
# you can afford without going out of memory (since larger batches will usually 
# result in faster evaluation/prediction).
# * Epoch: an arbitrary cutoff, generally defined as "one pass over the entire dataset", 
# used to separate training into distinct phases, which is useful for logging and 
# periodic evaluation.
# * When using validation_data or validation_split with the fit method of Keras models, 
# evaluation will be run at the end of every epoch.
# * Within Keras, there is the ability to add callbacks specifically designed to be 
# run at the end of an epoch. Examples of these are learning rate changes and model 
# checkpointing (saving).
model.fit(X_train,y_train,epochs=250)


# ## Evaluation
# 
# Let's evaluate our performance on our training set and our test set. We can compare 
# these two performances to check for overfitting.
print(model.history.history)
loss = model.history.history['loss']

sns.lineplot(x=range(len(loss)),y=loss)
plt.title("Training Loss per Epoch");
plt.savefig(PATH + 'loss.png', dpi=300)
plt.close()

# ### Compare final evaluation (MSE) on training set and test set.
# 
# These should hopefully be fairly close to each other.
print(model.metrics_names)
training_score = model.evaluate(X_train,y_train,verbose=0)
test_score = model.evaluate(X_test,y_test,verbose=0)
print(training_score)
print(test_score)

# ### Further Evaluations
test_predictions = model.predict(X_test)
print(test_predictions)

pred_df = pd.DataFrame(y_test,columns=['Test Y'])
print(pred_df)
test_predictions = pd.Series(test_predictions.reshape(300,))
print(test_predictions)
pred_df = pd.concat([pred_df,test_predictions],axis=1)
pred_df.columns = ['Test Y','Model Predictions']
print(pred_df)

# Let's compare to the real test labels!
sns.scatterplot(x='Test Y',y='Model Predictions',data=pred_df)
plt.savefig(PATH + 'preds.png', dpi=300)
plt.close()

pred_df['Error'] = pred_df['Test Y'] - pred_df['Model Predictions']
sns.distplot(pred_df['Error'],bins=50)
plt.savefig(PATH + 'error.png', dpi=300)
plt.close()

from sklearn.metrics import mean_absolute_error,mean_squared_error
print(mean_absolute_error(pred_df['Test Y'],pred_df['Model Predictions']))
print(mean_squared_error(pred_df['Test Y'],pred_df['Model Predictions']))

# Essentially the same thing, difference just due to precision
print(test_score)
#RMSE
print(test_score**0.5)

# # Predicting on brand new data
# 
# What if we just saw a brand new gemstone from the ground? What should we price it
# at? This is the **exact** same procedure as predicting on a new test data!
# [[Feature1, Feature2]]
new_gem = [[998,1000]]

# Don't forget to scale!
print(scaler.transform(new_gem))
new_gem = scaler.transform(new_gem)
print(model.predict(new_gem))

# ## Saving and Loading a Model
from tensorflow.keras.models import load_model
model.save('my_model.h5')  # creates a HDF5 file 'my_model.h5'
later_model = load_model('my_model.h5')
later_model.predict(new_gem)
