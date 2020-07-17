#!/usr/bin/env python
# coding: utf-8

# <a href="https://www.pieriandata.com"><img src="../Pierian_Data_Logo.PNG"></a>
# <strong><center>Copyright by Pierian Data Inc.</center></strong> 
# <strong><center>Created by Jose Marcial Portilla.</center></strong>

# # Keras API Project Exercise - Solutions
# 
# ## The Data
# 
# We will be using a subset of the LendingClub DataSet obtained from Kaggle: https://www.kaggle.com/wordsforthewise/lending-club
# 
# ## NOTE: Do not download the full zip from the link! We provide a special version 
# of this file that has some extra feature engineering for you to do. You won't be 
# able to follow along with the original file!
# 
# LendingClub is a US peer-to-peer lending company, headquartered in San Francisco, 
# California.[3] It was the first peer-to-peer lender to register its offerings as 
# securities with the Securities and Exchange Commission (SEC), and to offer loan 
# trading on a secondary market. LendingClub is the world's largest peer-to-peer lending platform.
# 
# ### Our Goal
# 
# Given historical data on loans given out with information on whether or not the 
# borrower defaulted (charge-off), can we build a model thatcan predict wether or 
# nor a borrower will pay back their loan? This way in the future when we get a new 
# potential customer we can assess whether or not they are likely to pay back the 
# loan. Keep in mind classification metrics when evaluating the performance of your model!
# 
# The "loan_status" column contains our label.
# 
# ### Data Overview

# ----
# -----
# There are many LendingClub data sets on Kaggle. Here is the information on this particular data set:
# 
# <table border="1" class="dataframe">
#   <thead>
#     <tr style="text-align: right;">
#       <th></th>
#       <th>LoanStatNew</th>
#       <th>Description</th>
#     </tr>
#   </thead>
#   <tbody>
#     <tr>
#       <th>0</th>
#       <td>loan_amnt</td>
#       <td>The listed amount of the loan applied for by the borrower. If at some 
#           point in time, the credit department reduces the loan amount, then it will
#           be reflected in this value.</td>
#     </tr>
#     <tr>
#       <th>1</th>
#       <td>term</td>
#       <td>The number of payments on the loan. Values are in months and can be either 36 or 60.</td>
#     </tr>
#     <tr>
#       <th>2</th>
#       <td>int_rate</td>
#       <td>Interest Rate on the loan</td>
#     </tr>
#     <tr>
#       <th>3</th>
#       <td>installment</td>
#       <td>The monthly payment owed by the borrower if the loan originates.</td>
#     </tr>
#     <tr>
#       <th>4</th>
#       <td>grade</td>
#       <td>LC assigned loan grade</td>
#     </tr>
#     <tr>
#       <th>5</th>
#       <td>sub_grade</td>
#       <td>LC assigned loan subgrade</td>
#     </tr>
#     <tr>
#       <th>6</th>
#       <td>emp_title</td>
#       <td>The job title supplied by the Borrower when applying for the loan.*</td>
#     </tr>
#     <tr>
#       <th>7</th>
#       <td>emp_length</td>
#       <td>Employment length in years. Possible values are between 0 and 10 where 0
#           means less than one year and 10 means ten or more years.</td>
#     </tr>
#     <tr>
#       <th>8</th>
#       <td>home_ownership</td>
#       <td>The home ownership status provided by the borrower during registration or 
#           obtained from the credit report. Our values are: RENT, OWN, MORTGAGE, OTHER</td>
#     </tr>
#     <tr>
#       <th>9</th>
#       <td>annual_inc</td>
#       <td>The self-reported annual income provided by the borrower during registration.</td>
#     </tr>
#     <tr>
#       <th>10</th>
#       <td>verification_status</td>
#       <td>Indicates if income was verified by LC, not verified, or if the income 
            # source was verified</td>
#     </tr>
#     <tr>
#       <th>11</th>
#       <td>issue_d</td>
#       <td>The month which the loan was funded</td>
#     </tr>
#     <tr>
#       <th>12</th>
#       <td>loan_status</td>
#       <td>Current status of the loan</td>
#     </tr>
#     <tr>
#       <th>13</th>
#       <td>purpose</td>
#       <td>A category provided by the borrower for the loan request.</td>
#     </tr>
#     <tr>
#       <th>14</th>
#       <td>title</td>
#       <td>The loan title provided by the borrower</td>
#     </tr>
#     <tr>
#       <th>15</th>
#       <td>zip_code</td>
#       <td>The first 3 numbers of the zip code provided by the borrower in the loan application.</td>
#     </tr>
#     <tr>
#       <th>16</th>
#       <td>addr_state</td>
#       <td>The state provided by the borrower in the loan application</td>
#     </tr>
#     <tr>
#       <th>17</th>
#       <td>dti</td>
#       <td>A ratio calculated using the borrower’s total monthly debt payments 
#           on the total debt obligations, excluding mortgage and the requested LC 
#           loan, divided by the borrower’s self-reported monthly income.</td>
#     </tr>
#     <tr>
#       <th>18</th>
#       <td>earliest_cr_line</td>
#       <td>The month the borrower's earliest reported credit line was opened</td>
#     </tr>
#     <tr>
#       <th>19</th>
#       <td>open_acc</td>
#       <td>The number of open credit lines in the borrower's credit file.</td>
#     </tr>
#     <tr>
#       <th>20</th>
#       <td>pub_rec</td>
#       <td>Number of derogatory public records</td>
#     </tr>
#     <tr>
#       <th>21</th>
#       <td>revol_bal</td>
#       <td>Total credit revolving balance</td>
#     </tr>
#     <tr>
#       <th>22</th>
#       <td>revol_util</td>
#       <td>Revolving line utilization rate, or the amount of credit the borrower 
#           is using relative to all available revolving credit.</td>
#     </tr>
#     <tr>
#       <th>23</th>
#       <td>total_acc</td>
#       <td>The total number of credit lines currently in the borrower's credit file</td>
#     </tr>
#     <tr>
#       <th>24</th>
#       <td>initial_list_status</td>
#       <td>The initial listing status of the loan. Possible values are – W, F</td>
#     </tr>
#     <tr>
#       <th>25</th>
#       <td>application_type</td>
#       <td>Indicates whether the loan is an individual application or a joint 
#           application with two co-borrowers</td>
#     </tr>
#     <tr>
#       <th>26</th>
#       <td>mort_acc</td>
#       <td>Number of mortgage accounts.</td>
#     </tr>
#     <tr>
#       <th>27</th>
#       <td>pub_rec_bankruptcies</td>
#       <td>Number of public record bankruptcies</td>
#     </tr>
#   </tbody>
# </table>
# 
# ---
# ----

# ## Starter Code
# 
# #### Note: We also provide feature information on the data as a .csv file for
#       easy lookup throughout the notebook:
import pandas as pd
import numpy as np
PATH = '/home/ec2-user/environment/udemy_courses/data_science_py/25_nn/figs/'
data_info = pd.read_csv('../DATA/lending_club_info.csv',index_col='LoanStatNew')
print(data_info.loc['revol_util']['Description'])

def feat_info(col_name):
    print(data_info.loc[col_name]['Description'])

print(feat_info('mort_acc'))

# ## Loading the data and other imports
import matplotlib.pyplot as plt
import seaborn as sns

# might be needed depending on your version of Jupyter
# get_ipython().run_line_magic('matplotlib', 'inline')
df = pd.read_csv('../DATA/lending_club_loan_two.csv')
print(df.info())

# # Project Tasks
# 
# **Complete the tasks below! Keep in mind is usually more than one way to complete the task! Enjoy**
# 
# -----
# ------
# 
# # Section 1: Exploratory Data Analysis
# 
# **OVERALL GOAL: Get an understanding for which variables are important, view 
#   summary statistics, and visualize the data**
# 
# 
# ----
# **TASK: Since we will be attempting to predict loan_status, create a countplot as shown below.**
sns.countplot(x='loan_status',data=df)
plt.savefig(PATH + 'loan_status.png', dpi=300)
plt.close()

# **TASK: Create a histogram of the loan_amnt column.**
plt.figure(figsize=(12,4))
sns.distplot(df['loan_amnt'],kde=False,bins=40)
plt.xlim(0,45000)
plt.savefig(PATH + 'loan_amt.png', dpi=300)
plt.close()

# **TASK: Let's explore correlation between the continuous feature variables. Calculate 
# the correlation between all continuous numeric variables using .corr() method.**
print(df.corr())


# **TASK: Visualize this using a heatmap. Depending on your version of matplotlib, 
# you may need to manually adjust the heatmap.**
# 
# * [Heatmap info](https://seaborn.pydata.org/generated/seaborn.heatmap.html#seaborn.heatmap)
# * [Help with resizing](https://stackoverflow.com/questions/56942670/matplotlib-seaborn-first-and-last-row-cut-in-half-of-heatmap-plot)
plt.figure(figsize=(12,7))
sns.heatmap(df.corr(),annot=True,cmap='viridis')
plt.ylim(10, 0)
plt.savefig(PATH + 'corr.png', dpi=300)
plt.close()


# **TASK: You should have noticed almost perfect correlation with the "installment" 
# feature. Explore this feature further. Print out their descriptions and perform a 
# scatterplot between them. Does this relationship make sense to you? Do you think
# there is duplicate information here?**
print(feat_info('installment'))
print(feat_info('loan_amnt'))

sns.scatterplot(x='installment',y='loan_amnt',data=df,)
plt.savefig(PATH + 'installment.png', dpi=300)
plt.close()

# **TASK: Create a boxplot showing the relationship between the loan_status and the Loan Amount.**
sns.boxplot(x='loan_status',y='loan_amnt',data=df)
plt.savefig(PATH + 'loan_box.png', dpi=300)
plt.close()

# **TASK: Calculate the summary statistics for the loan amount, grouped by the loan_status.**
print(df.groupby('loan_status')['loan_amnt'].describe())

# **TASK: Let's explore the Grade and SubGrade columns that LendingClub attributes
# to the loans. What are the unique possible grades and subgrades?**
print(sorted(df['grade'].unique()))
print(sorted(df['sub_grade'].unique()))


# **TASK: Create a countplot per grade. Set the hue to the loan_status label.**
sns.countplot(x='grade',data=df,hue='loan_status')
plt.savefig(PATH + 'grade.png', dpi=300)
plt.close()

# **TASK: Display a count plot per subgrade. You may need to resize for this plot 
# and reorder the x axis. Feel free to edit the color palette. Explore both all 
# loans made per subgrade as well being separated based on the loan_status**
plt.figure(figsize=(12,4))
subgrade_order = sorted(df['sub_grade'].unique())
sns.countplot(x='sub_grade',data=df,order = subgrade_order,palette='coolwarm' )
plt.savefig(PATH + 'subgrade.png', dpi=300)
plt.close()

plt.figure(figsize=(12,4))
subgrade_order = sorted(df['sub_grade'].unique())
sns.countplot(x='sub_grade',data=df,order = subgrade_order,palette='coolwarm' ,hue='loan_status')
plt.savefig(PATH + 'subgrde_loan.png', dpi=300)
plt.close()

# **TASK: It looks like F and G subgrades don't get paid back that often. 
# Isloate those and recreate the countplot just for those subgrades.**
f_and_g = df[(df['grade']=='G') | (df['grade']=='F')]
plt.figure(figsize=(12,4))
subgrade_order = sorted(f_and_g['sub_grade'].unique())
sns.countplot(x='sub_grade',data=f_and_g,order = subgrade_order,hue='loan_status')
plt.savefig(PATH + 'f_g_grade.png', dpi=300)
plt.close()

# **TASK: Create a new column called 'load_repaid' which will contain a 1 if the
# loan status was "Fully Paid" and a 0 if it was "Charged Off".**
print(df['loan_status'].unique())
df['loan_repaid'] = df['loan_status'].map({'Fully Paid':1,'Charged Off':0})
print(df[['loan_repaid','loan_status']])

# **CHALLENGE TASK: (Note this is hard, but can be done in one line!) Create a bar 
# plot showing the correlation of the numeric features to the new loan_repaid column.
# [Helpful Link](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.bar.html)**
print(df.corr()['loan_repaid'].sort_values().drop('loan_repaid').plot(kind='bar'))

# ---
# ---
# # Section 2: Data PreProcessing
# 
# **Section Goals: Remove or fill any missing data. Remove unnecessary or repetitive
# features. Convert categorical string features to dummy variables.**
# 
# 
print(df.head())

# # Missing Data
# 
# **Let's explore this missing data columns. We use a variety of factors to decide
# whether or not they would be useful, to see if we should keep, discard, or fill 
# in the missing data.**
# **TASK: What is the length of the dataframe?**
print(len(df))

# **TASK: Create a Series that displays the total count of missing values per column.**
print(df.isnull().sum())

# **TASK: Convert this Series to be in term of percentage of the total DataFrame**
print(100* df.isnull().sum()/len(df))

# **TASK: Let's examine emp_title and emp_length to see whether it will be okay 
# to drop them. Print out their feature information using the feat_info() function 
# from the top of this notebook.**
print(feat_info('emp_title'))
print('\n')
print(feat_info('emp_length'))

# **TASK: How many unique employment job titles are there?**
print(df['emp_title'].nunique())
print(df['emp_title'].value_counts())

# **TASK: Realistically there are too many unique job titles to try to convert 
# this to a dummy variable feature. Let's remove that emp_title column.**
df = df.drop('emp_title',axis=1)

# **TASK: Create a count plot of the emp_length feature column. Challenge: Sort the order of the values.**
print(sorted(df['emp_length'].dropna().unique()))
emp_length_order = [ '< 1 year',
                      '1 year',
                     '2 years',
                     '3 years',
                     '4 years',
                     '5 years',
                     '6 years',
                     '7 years',
                     '8 years',
                     '9 years',
                     '10+ years']
plt.figure(figsize=(12,4))
sns.countplot(x='emp_length',data=df,order=emp_length_order)
plt.savefig(PATH + 'emp_len.png', dpi=300)
plt.close()

# **TASK: Plot out the countplot with a hue separating Fully Paid vs Charged Off**
plt.figure(figsize=(12,4))
sns.countplot(x='emp_length',data=df,order=emp_length_order,hue='loan_status')
plt.savefig(PATH + 'emp_loan.png', dpi=300)
plt.close()

# **CHALLENGE TASK: This still doesn't really inform us if there is a 
# strong relationship between employment length and being charged off, what we 
# want is the percentage of charge offs per category. Essentially informing us 
# what percent of people per employment category didn't pay back their loan. 
# There are a multitude of ways to create this Series. Once you've created it, 
# see if visualize it with a [bar plot](https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.DataFrame.plot.html). 
# This may be tricky, refer to solutions if you get stuck on creating this Series.**
emp_co = df[df['loan_status']=="Charged Off"].groupby("emp_length").count()['loan_status']
emp_fp = df[df['loan_status']=="Fully Paid"].groupby("emp_length").count()['loan_status']
emp_len = emp_co/emp_fp
print(emp_len)
emp_len.plot(kind='bar')
plt.savefig(PATH + 'emp_len_bar.png', dpi=300)
plt.close()

# **TASK: Charge off rates are extremely similar across all employment lengths. 
# Go ahead and drop the emp_length column.**
df = df.drop('emp_length',axis=1)


# **TASK: Revisit the DataFrame to see what feature columns still have missing data.**
print(df.isnull().sum())

# **TASK: Review the title column vs the purpose column. Is this repeated information?**
print(df['purpose'].head(10))
print(df['title'].head(10))

# **TASK: The title column is simply a string subcategory/description of the purpose 
# column. Go ahead and drop the title column.**
df = df.drop('title',axis=1)

# ---
# **NOTE: This is one of the hardest parts of the project! Refer to the solutions
# video if you need guidance, feel free to fill or drop the missing values of the 
# mort_acc however you see fit! Here we're going with a very specific approach.**
# 
# 
# ---
# **TASK: Find out what the mort_acc feature represents**
print(feat_info('mort_acc'))

# **TASK: Create a value_counts of the mort_acc column.**
print(df['mort_acc'].value_counts())

# **TASK: There are many ways we could deal with this missing data. We could 
# attempt to build a simple model to fill it in, such as a linear model, we could
# just fill it in based on the mean of the other columns, or you could even bin the 
# columns into categories and then set NaN as its own category. There is no 100% 
# correct approach! Let's review the other columsn to see which most highly correlates to mort_acc**
print("Correlation with the mort_acc column")
print(df.corr()['mort_acc'].sort_values())


# **TASK: Looks like the total_acc feature correlates with the mort_acc , this makes 
# sense! Let's try this fillna() approach. We will group the dataframe by the total_acc
# and calculate the mean value for the mort_acc per total_acc entry. To get the result below:**
print("Mean of mort_acc column per total_acc")
print(df.groupby('total_acc').mean()['mort_acc'])

# **CHALLENGE TASK: Let's fill in the missing mort_acc values based on their 
# total_acc value. If the mort_acc is missing, then we will fill in that missing value 
# with the mean value corresponding to its total_acc value from the Series we created
# above. This involves using an .apply() method with two columns. Check out the link
# below for more info, or review the solutions video/notebook.**
# 
# [Helpful Link](https://stackoverflow.com/questions/13331698/how-to-apply-a-function-to-two-columns-of-pandas-dataframe) 
total_acc_avg = df.groupby('total_acc').mean()['mort_acc']
print(total_acc_avg[2.0])

def fill_mort_acc(total_acc,mort_acc):
    '''
    Accepts the total_acc and mort_acc values for the row.
    Checks if the mort_acc is NaN , if so, it returns the avg mort_acc value
    for the corresponding total_acc value for that row.
    
    total_acc_avg here should be a Series or dictionary containing the mapping of the
    groupby averages of mort_acc per total_acc values.
    '''
    if np.isnan(mort_acc):
        return total_acc_avg[total_acc]
    else:
        return mort_acc

df['mort_acc'] = df.apply(lambda x: fill_mort_acc(x['total_acc'], x['mort_acc']), axis=1)
print(df.isnull().sum())

# **TASK: revol_util and the pub_rec_bankruptcies have missing data points, 
# but they account for less than 0.5% of the total data. Go ahead and remove the 
# rows that are missing those values in those columns with dropna().**
df = df.dropna()
print(df.isnull().sum())

# ## Categorical Variables and Dummy Variables
# 
# **We're done working with the missing data! Now we just need to deal with the 
# string values due to the categorical columns.**
# 
# **TASK: List all the columns that are currently non-numeric. [Helpful Link](https://stackoverflow.com/questions/22470690/get-list-of-pandas-dataframe-columns-based-on-data-type)**
# 
# [Another very useful method call](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.select_dtypes.html)
print(df.select_dtypes(['object']).columns)

# ---
# **Let's now go through all the string features to see what we should do with them.**
# 
# ---
# 
# 
# ### term feature
# 
# **TASK: Convert the term feature into either a 36 or 60 integer numeric data type using .apply() or .map().**
print(df['term'].value_counts())
# Or just use .map()
df['term'] = df['term'].apply(lambda term: int(term[:3]))

# ### grade feature
# 
# **TASK: We already know grade is part of sub_grade, so just drop the grade feature.**
df = df.drop('grade',axis=1)

# **TASK: Convert the subgrade into dummy variables. Then concatenate these new 
# columns to the original dataframe. Remember to drop the original subgrade column 
# and to add drop_first=True to your get_dummies call.**
subgrade_dummies = pd.get_dummies(df['sub_grade'],drop_first=True)
df = pd.concat([df.drop('sub_grade',axis=1),subgrade_dummies],axis=1)
print(df.columns)
print(df.select_dtypes(['object']).columns)

# ### verification_status, application_type,initial_list_status,purpose 
# **TASK: Convert these columns: ['verification_status', 'application_type','initial_list_status','purpose'] 
# into dummy variables and concatenate them with the original dataframe. Remember 
# to set drop_first=True and to drop the original columns.**
dummies = pd.get_dummies(df[['verification_status', 'application_type','initial_list_status','purpose' ]],drop_first=True)
df = df.drop(['verification_status', 'application_type','initial_list_status','purpose'],axis=1)
df = pd.concat([df,dummies],axis=1)

# ### home_ownership
# **TASK:Review the value_counts for the home_ownership column.**
print(df['home_ownership'].value_counts())

# **TASK: Convert these to dummy variables, but [replace](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.replace.html) 
# NONE and ANY with OTHER, so that we end up with just 4 categories, 
# MORTGAGE, RENT, OWN, OTHER. Then concatenate them with the original dataframe. 
# Remember to set drop_first=True and to drop the original columns.**
df['home_ownership']=df['home_ownership'].replace(['NONE', 'ANY'], 'OTHER')
dummies = pd.get_dummies(df['home_ownership'],drop_first=True)
df = df.drop('home_ownership',axis=1)
df = pd.concat([df,dummies],axis=1)

# ### address
# **TASK: Let's feature engineer a zip code column from the address in the data set. 
# Create a column called 'zip_code' that extracts the zip code from the address column.**
df['zip_code'] = df['address'].apply(lambda address:address[-5:])

# **TASK: Now make this zip_code column into dummy variables using pandas. 
# Concatenate the result and drop the original zip_code column along with dropping the address column.**
dummies = pd.get_dummies(df['zip_code'],drop_first=True)
df = df.drop(['zip_code','address'],axis=1)
df = pd.concat([df,dummies],axis=1)

# ### issue_d 
# 
# **TASK: This would be data leakage, we wouldn't know beforehand whether or not a 
# loan would be issued when using our model, so in theory we wouldn't have an issue_date, drop this feature.**
df = df.drop('issue_d',axis=1)

# ### earliest_cr_line
# **TASK: This appears to be a historical time stamp feature. Extract the year from 
# this feature using a .apply function, then convert it to a numeric feature. Set this 
# new data to a feature column called 'earliest_cr_year'.Then drop the earliest_cr_line feature.**
df['earliest_cr_year'] = df['earliest_cr_line'].apply(lambda date:int(date[-4:]))
df = df.drop('earliest_cr_line',axis=1)
print(df.select_dtypes(['object']).columns)


# ## Train Test Split
# **TASK: Import train_test_split from sklearn.**
from sklearn.model_selection import train_test_split

# **TASK: drop the load_status column we created earlier, since its a duplicate of the 
# loan_repaid column. We'll use the loan_repaid column since its already in 0s and 1s.**
df = df.drop('loan_status',axis=1)

# **TASK: Set X and y variables to the .values of the features and label.**
X = df.drop('loan_repaid',axis=1).values
y = df['loan_repaid'].values

# ----
# ----
# 
# # OPTIONAL
# 
# ## Grabbing a Sample for Training Time
# 
# ### OPTIONAL: Use .sample() to grab a sample of the 490k+ entries to save time on
# training. Highly recommended for lower RAM computers or if you are not using GPU.
# 
# ----
# ----
# df = df.sample(frac=0.1,random_state=101)
print(len(df))

# **TASK: Perform a train/test split with test_size=0.2 and a random_state of 101.**
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=101)

# ## Normalizing the Data
# 
# **TASK: Use a MinMaxScaler to normalize the feature data X_train and X_test. 
# Recall we don't want data leakge from the test set so we only fit on the X_train data.**
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# # Creating the Model
# 
# **TASK: Run the cell below to import the necessary Keras functions.**
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation,Dropout
from tensorflow.keras.constraints import max_norm
# **TASK: Build a sequential model to will be trained on the data. You have unlimited 
# options here, but here is what the solution uses: a model that 
# goes 78 --> 39 --> 19--> 1 output neuron. OPTIONAL: Explore adding
# [Dropout layers](https://keras.io/layers/core/) [1](https://en.wikipedia.org/wiki/Dropout_(neural_networks)) 
# [2](https://towardsdatascience.com/machine-learning-part-20-dropout-keras-layers-explained-8c9f6dc4c9ab)**
model = Sequential()

# Choose whatever number of layers/neurons you want.
# https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw
# Remember to compile()
model = Sequential()
# https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw

# input layer
model.add(Dense(78,  activation='relu'))
model.add(Dropout(0.2))

# hidden layer
model.add(Dense(39, activation='relu'))
model.add(Dropout(0.2))

# hidden layer
model.add(Dense(19, activation='relu'))
model.add(Dropout(0.2))

# output layer
model.add(Dense(units=1,activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam')

# **TASK: Fit the model to the training data for at least 25 epochs. Also add in 
# the validation data for later plotting. Optional: add in a batch_size of 256.**
model.fit(x=X_train, 
          y=y_train, 
          epochs=25,
          batch_size=256,
          validation_data=(X_test, y_test), 
          )

# **TASK: OPTIONAL: Save your model.**
from tensorflow.keras.models import load_model
model.save('full_data_project_model.h5')  

# # Section 3: Evaluating Model Performance.
# 
# **TASK: Plot out the validation loss versus the training loss.**
losses = pd.DataFrame(model.history.history)
losses[['loss','val_loss']].plot()
plt.savefig(PATH + 'losses_val_loss.png', dpi=300)
plt.close()

# **TASK: Create predictions from the X_test set and display a classification 
# report and confusion matrix for the X_test set.**
from sklearn.metrics import classification_report,confusion_matrix
predictions = model.predict_classes(X_test)
print(classification_report(y_test,predictions))
print(confusion_matrix(y_test,predictions))

# **TASK: Given the customer below, would you offer this person a loan?**
import random
random.seed(101)
random_ind = random.randint(0,len(df))

new_customer = df.drop('loan_repaid',axis=1).iloc[random_ind]
print(new_customer)
print(model.predict_classes(new_customer.values.reshape(1,78)))

# **TASK: Now check, did this person actually end up paying back their loan?**
print(df.iloc[random_ind]['loan_repaid'])

# # GREAT JOB!