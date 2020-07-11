#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___
# # Logistic Regression with Python
# 
# For this lecture we will be working with the [Titanic Data Set from Kaggle](https://www.kaggle.com/c/titanic).
# This is a very famous data set and very often is a student's first step in machine learning! 
# 
# We'll be trying to predict a classification- survival or deceased.
# Let's begin our understanding of implementing Logistic Regression in Python for classification.
# 
# We'll use a "semi-cleaned" version of the titanic data set, if you use the data set
# hosted directly on Kaggle, you may need to do some additional cleaning not 
# shown in this lecture notebook.
# 
# ## Import Libraries
# Let's import some libraries to get started!
import sys, pdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
PATH = '/home/ec2-user/environment/udemy_courses/data_science_py/17_logistic_regression/figs/'

# ## The Data
# 
# Let's start by reading in the titanic_train.csv file into a pandas dataframe.
train = pd.read_csv('titanic_train.csv')
print(train.head())

# # Exploratory Data Analysis
# 
# Let's begin some exploratory data analysis! We'll start by checking out missing data!
# 
# ## Missing Data
# 
# We can use seaborn to create a simple heatmap to see where we are missing data!
sns.heatmap(train.isnull(),yticklabels=False,cbar=False,cmap='viridis')
plt.savefig(PATH + 'titanic_heatmap.png', dpi=300)
plt.close()

# Roughly 20 percent of the Age data is missing. The proportion of Age missing is 
# likely small enough for reasonable replacement with some form of imputation. 
# Looking at the Cabin column, it looks like we are just missing too much of that 
# data to do something useful with at a basic level. We'll probably drop this 
# later, or change it to another feature like "Cabin Known: 1 or 0"
# 
# Let's continue on by visualizing some more of the data! Check out the video for
# full explanations over these plots, this code is just to serve as reference.
sns.set_style('whitegrid')
sns.countplot(x='Survived',data=train,palette='RdBu_r')
plt.savefig(PATH + 'titanic_count.png', dpi=300)
plt.close()

sns.set_style('whitegrid')
sns.countplot(x='Survived',hue='Sex',data=train,palette='RdBu_r')
plt.savefig(PATH + 'titanic_count_sex.png', dpi=300)
plt.close()

sns.set_style('whitegrid')
sns.countplot(x='Survived',hue='Pclass',data=train,palette='rainbow')
plt.savefig(PATH + 'titanic_class.png', dpi=300)
plt.close()

sns.distplot(train['Age'].dropna(),kde=False,color='darkred',bins=30)
plt.savefig(PATH + 'dist_age.png', dpi=300)
plt.close()

train['Age'].hist(bins=30,color='darkred',alpha=0.7)
plt.savefig(PATH + 'titanic_age_hist.png', dpi=300)
plt.close()

sns.countplot(x='SibSp',data=train)
plt.savefig(PATH + 'sibsp_count.png', dpi=300)
plt.close()

train['Fare'].hist(color='green',bins=40,figsize=(8,4))
plt.savefig(PATH + 'fare_hist.png', dpi=300)
plt.close()

# ____
# ### Cufflinks for plots
# ___
#  Let's take a quick moment to show an example of cufflinks!
import cufflinks as cf
cf.go_offline()

# train['Fare'].iplot(kind='hist',bins=30,color='green')

# ___
# ## Data Cleaning
# We want to fill in missing age data instead of just dropping the missing age 
# data rows. One way to do this is by filling in the mean age of all the passengers (imputation).
# However we can be smarter about this and check the average age by passenger class. For example:
# 
plt.figure(figsize=(12, 7))
sns.boxplot(x='Pclass',y='Age',data=train,palette='winter')
plt.savefig(PATH + 'age_hist.png', dpi=300)
plt.close()

# We can see the wealthier passengers in the higher classes tend to be older, 
# which makes sense. We'll use these average age values to impute based on Pclass for Age.
def impute_age(cols):
    Age = cols[0]
    Pclass = cols[1]
    
    if pd.isnull(Age):
        if Pclass == 1:
            return 37
        elif Pclass == 2:
            return 29
        else:
            return 24
    else:
        return Age

# Now apply that function!
train['Age'] = train[['Age','Pclass']].apply(impute_age,axis=1)

# Now let's check that heat map again!
sns.heatmap(train.isnull(),yticklabels=False,cbar=False,cmap='viridis')
plt.savefig(PATH + 'class_heatmap.png', dpi=300)
plt.close()

# Great! Let's go ahead and drop the Cabin column and the row in Embarked that is NaN.
train.drop('Cabin',axis=1,inplace=True)
print(train.head())
train.dropna(inplace=True)

# ## Converting Categorical Features 
# 
# We'll need to convert categorical features to dummy variables using pandas! 
# Otherwise our machine learning algorithm won't be able to directly take in 
# those features as inputs.
print(train.info())

sex = pd.get_dummies(train['Sex'],drop_first=True)
embark = pd.get_dummies(train['Embarked'],drop_first=True)
train.drop(['Sex','Embarked','Name','Ticket'],axis=1,inplace=True)
train = pd.concat([train,sex,embark],axis=1)
print(train.head())

# Great! Our data is ready for our model!
# 
# # Building a Logistic Regression model
# 
# Let's start by splitting our data into a training set and test set 
# (there is another test.csv file that you can play around with in case you 
# want to use all this data for training).
# 
# ## Train Test Split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(train.drop('Survived',axis=1), 
                                                    train['Survived'], test_size=0.30, 
                                                    random_state=101)

# ## Training and Predicting
from sklearn.linear_model import LogisticRegression

logmodel = LogisticRegression()
logmodel.fit(X_train,y_train)
predictions = logmodel.predict(X_test)

# Let's move on to evaluate our model!
# ## Evaluation
# We can check precision,recall,f1-score using classification report!
from sklearn.metrics import classification_report
print(classification_report(y_test,predictions))

# Not so bad! You might want to explore other feature engineering and the other titanic_text.csv file, some suggestions for feature engineering:
# 
# * Try grabbing the Title (Dr.,Mr.,Mrs,etc..) from the name as a feature
# * Maybe the Cabin letter could be a feature
# * Is there any info you can get from the ticket?
# 
# ## Great Job!
