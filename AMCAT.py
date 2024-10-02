#!/usr/bin/env python
# coding: utf-8

# In[5]:


#importing relevent libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats as st


# In[2]:


df = pd.read_csv("C:\\Users\\91939\\Downloads\\data.xlsx - Sheet1.csv")


# In[3]:


df.head()


# In[6]:


#shape of the dataset
df.shape


# In[7]:


#size of the dataset
df.size


# In[9]:


#removing the unknown column
df.drop("Unnamed: 0",axis = 1,inplace = True)


# In[10]:


df.head()


# In[11]:


#checking the info of the dataset
df.info()


# In[12]:


#columns
df.columns


# In[13]:


#fixing the datatypes
df['DOJ'] = pd.to_datetime(df['DOJ'])


# In[65]:


df.info()


# In[66]:


#checking missing values
df.isna().sum()


# In[67]:


#checking duplicate values
df.duplicated().sum()


# # Univariate Analysis 
# 

# Analysing the data using single variable

# In[68]:


#distribution of target variable(salary)
pd.DataFrame(df["Salary"].describe())


# In[69]:


#plotting kde plot 
sns.kdeplot(data = df["Salary"])
plt.grid()
plt.title("Distribution of Salary")
plt.show()


# observations 

# In between 0 to 100000 the salaries are more compare to other salaries
# 

# After 300000 salaries are less

# In[70]:


df["collegeGPA"].mean()


# In[77]:


pd.DataFrame(df["JobCity"].value_counts())


# In[85]:


#finding which specialization is most common
specialization_counts=df["Specialization"].value_counts().head(10)
d1 = pd.DataFrame(specialization_counts)
d1.columns = ["Count"]
d1 = d1.reset_index()
d1.columns = ['Specialization','Count']
print(d1)


# In[89]:


#barplot
plt.figure(figsize=(8,6))
sns.barplot(y=d1['Specialization'],x=d1['Count'],palette="muted")
plt.title("Distribution of Specialization")
plt.xlabel("Count")
plt.ylabel("Specialization")
plt.tight_layout()
plt.show()


# #observations:

# electronics and communication engineering students are more

# electronics & instrumentation eng are less

# In[90]:


#plotting the graphs on columns
c_columns = len(df.columns)
#choosing 3columns per row
r_rows = int(np.ceil(c_columns / 3))


# In[96]:


fig, axes = plt.subplots(r_rows, 3, figsize=(20, r_rows*6))
axes = axes.flatten()
#iterating over each column in the dataframe
for i, columns in enumerate(df.columns):
    #if the column is categorical
    if df[columns].dtype == "object" or df[columns].dtype == "category":
        sns.countplot(x=columns, data=df, ax=axes[i])
        axes[i].set_title(f'Distribution of{columns} (Categorical)')
        #if column is datetime
    elif pd.api.types.is_datetime64_any_dtype(df[columns]):
        df[columns] = pd.to_datetime(df[columns])
        df[columns].value_counts().sort_index().plot(ax=axes[i])
        axes[i].set_title(f'Time Distribution of {columns} (Datetime)')
        axes[i].set_xlabel("Date")
        axes[i].set_ylabel("Count")
        #if column is numeric
    elif pd.api.types.is_numeric_dtype(df[columns]):
        sns.histplot(df[columns], kde=True, ax=axes[i])
        axes[i].set_title(f'Distribution of {columns} (Numerical)')
    if i>=c_columns:
        axes[i].axes("off")
plt.show()
    


# #outliers in each numerical column:
# 

# In[97]:


for i in df.columns:
    if df[i].dtype=="int" or df[i].dtype=="float":
        sns.boxplot(x=df[i])
        plt.title("Boxplot for {}".format(i))
        plt.show()


#  The frequency distribution of each categorical Variable

# In[99]:


for i in df.columns:
    if df[i].dtype=="object":
        sns.barplot(x=df[i].unique()[:10],y=df[i].value_counts()[:10])
        plt.title("Distribution of {}".format(i))
        plt.xticks(rotation=90)
        plt.show()


# # Bivariate Analysis

# Analysing data using two variables

# #The relationships between numerical columns using scatter plot:

# In[103]:


sns.scatterplot(x="collegeGPA", y="Salary",data=df)
plt.title("Scatter plot of collegGPA vs Salary")
plt.show()


#  #categorical vs numerical columns using box plot:

# In[106]:


sns.boxplot(x="Degree", y="Salary", data = df)
plt.title("Box plot of degree vs salary")
plt.show()


# #Relationships between categorical vs categorical columns using stacked bar plots:
#  

# In[109]:


pd.crosstab(df['CollegeState'], df['Gender']).plot(kind='bar', stacked=True)
plt.title('Stacked Bar Plot Gneder vs Designation')
plt.show()


# # Research Questions
# 
# 

# In[123]:


from scipy import stats

# Filter the data for relevant job roles
relevant_roles = ['programmer Analyst', 'software engineer', 'hardware engineer', 'associate engineer']
df_filtered = df[df['Designation'].isin(relevant_roles)]
salary_data = df_filtered["Salary"]
claimed_mean_salary = 2.75*100000

t_stat, p_value = stats.ttest_1samp(salary_data, claimed_mean_salary)

print(f"Mean Salary of Selected Roles: {salary_data.mean():.2f}")
print(f"Claimed Mean Salary: {claimed_mean_salary:.2f}")


print(f"T-statistic: {t_stat:.2f}")
print(f"p-value: {p_value:.4f}")

alpha = 0.05

if p_value < alpha:
      print("Reject the null hypothesis: The average salary is significantly different from the claimed mean.")
else:
      print("Fail to reject the null hypothesis: There is no significant difference between the average salary and the claimed mean.")


# In[125]:


from scipy import stats as st
from scipy.stats import chi2_contingency
# Create a contingency table
contingency_table = pd.crosstab(index = df['Specialization'], columns = df['Gender'])

# Chi-square test of independence
chi2_stat, p_val, dof, expected = chi2_contingency(contingency_table)
if p_value < alpha:
    print("Reject the null hypothesis: There is a significant difference between the gender and speciliazation.")
else:
    print("Fail to reject the null hypothesis: There is no significant difference between the gende and specilization.")




# In[ ]:




