#!/usr/bin/env python
# coding: utf-8

# In[2]:

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#https://www.kaggle.com/datasets/fatihilhan/electric-vehicle-specifications-and-prices/data

#Adding a white background with gridlines to increase readability of the plots
sns.set(style="whitegrid")


# In[3]:

df = pd.read_csv('data\EV_cars.csv')
df


# In[30]:


#Price distribution of 360 EVs

plt.figure(figsize=(12, 6))
sns.histplot(df['Price.DE.'], bins=30, kde=True, color='#2F5597')
plt.title('Price Distribution of Electric Vehicles')
plt.xlabel('Price (EUR)')
plt.ylabel('Frequency')
plt.axvline(df['Price.DE.'].mean(), color='red', linestyle='--', label='Mean Price')
plt.axvline(df['Price.DE.'].median(), color='black', linestyle='--', label='Median Price')
plt.legend()
plt.show()


# In[20]:


#Price vs Range

#Creating the scatterplot
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Range', y='Price.DE.', data=df, color='blue')
plt.title('Price vs. Range')
plt.xlabel('Range (km)')
plt.ylabel('Price (EUR)')
plt.show()


# In[24]:


#Price Categories vs Range

#Creating price bins of 10k, from under 30k to over 70k
price_bins = [0, 30000, 40000, 50000, 60000, 70000, 80000, 100000, 200000]
price_labels = ['<30k', '30-40k', '40-50k', '50-60k', '60-70k', '70k-80k', '80k-100k', '>100k']

# Creating a new attribute for price category
df['Price_category'] = pd.cut(df['Price.DE.'], bins=price_bins, labels=price_labels)

#Creating the boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(x='Price_category', y='Range', data=df, palette='Blues')
plt.title('Price Categories vs Range')
plt.xlabel('Price Category (EUR)')
plt.ylabel('Range (km)')
plt.xticks(rotation=45)
plt.show()


# In[25]:


#Efficiency comparison by price ranges of 10k

# Calculate the average efficiency by price category
efficiency_by_price = df.groupby('Price_category')['Efficiency'].mean().reset_index()

#Creating the barplot
plt.figure(figsize=(10, 6))
sns.barplot(x='Efficiency', y='Price_category', data=efficiency_by_price, palette='Blues')
plt.title('Price categories vs Efficiency')
plt.xlabel('Average Efficiency (Wh/km)')
plt.ylabel('Price Range (EUR)')
plt.show()


# In[61]:


#Price vs Charging time in minutes

#Creating the scatterplot
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Price.DE.', y='Fast_charge', data=df, color='blue', alpha=0.7)
plt.title('Price vs. Fast-Charging Time')
plt.xlabel('Price (EUR)')
plt.ylabel('Fast Charging Time (minutes)')
plt.legend()
plt.show()


# In[26]:


#Price categories vs Fast charging time in minutes 

#Calculating the average fast charge
avg_fast_charge = df.groupby('Price_category')['Fast_charge'].mean().reset_index()

#Creating the barplot
plt.figure(figsize=(10, 6))
sns.barplot(x='Price_category', y='Fast_charge', data=avg_fast_charge, palette='Blues')
plt.title('Price categories vs Fast-Charging Time')
plt.xlabel('Price Category (EUR)')
plt.ylabel('Fast-Charging Time (minutes)')
plt.show()


# In[19]:


#Price vs Acceleration

#Creating the scatterplot
plt.figure(figsize=(10, 6))
sns.scatterplot(x='acceleration..0.100.', y='Price.DE.', data=df , color='blue')
plt.title('Price vs Acceleration')
plt.xlabel('Acceleration (0-100 km/h, seconds)')
plt.ylabel('Price (EUR)')
plt.show()


# In[53]:


#Price vs Top Speed

#Creating the scatterplot
plt.figure(figsize=(12, 6))
sns.scatterplot(x='Price.DE.', y='Top_speed', data=df, color='blue', alpha=0.7)
plt.title('Price vs Top Speed')
plt.xlabel('Price (EUR)')
plt.ylabel('Top Speed (km/h)')
plt.legend()
plt.show()


# In[16]:


#Price vs Battery Capacity

#Creating the scatterplot
plt.figure(figsize=(12, 6))
sns.scatterplot(x='Price.DE.', y='Battery', data=df, color='blue', alpha=0.7)
plt.title('Price vs Battery Capacity')
plt.xlabel('Price (EUR)')
plt.ylabel('Battery Capacity (kWh)')
plt.legend()
plt.show()


# In[ ]:




