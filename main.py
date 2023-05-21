import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tns
import seaborn as sn
import re

# Import and retrieve information about the dataset
df = pd.read_csv('finance_liquor_sales.csv')
df.info()
print(df.head())

#Check for null values
print(df.isnull().sum())

df = df.dropna()


#Convert date column type from object to date
df["date"] = pd.to_datetime(df["date"])

#Get the year from each date and filter the dataset

df_period = df[(df['date'].dt.year >= 2016) & (df['date'].dt.year <= 2019)]


#Export data to csv:

df_period.to_csv('new_dataset_2016_2019.csv', index=False)

#Aggregate the CSV data so we can get the most popular item

total_sales_per_item_per_store = df_period.groupby(['zip_code','item_description'])['bottles_sold'].sum().reset_index()  #use reset_index() to reset the Index of the Series and new DataFrame with
                                                                                                                      #the original index values as columns
total_sales_per_item_per_store.info()

most_popular = total_sales_per_item_per_store.groupby(['zip_code'])['bottles_sold'].max().reset_index()

most_popular_item_per_store = most_popular.merge(total_sales_per_item_per_store, on=['zip_code','bottles_sold'], how='left').sort_values('bottles_sold', ascending= False)

most_popular_item_per_store.to_csv('most_popular_items.csv', index=False)

print("\nThe most popular items witin each store are:\n", most_popular_item_per_store.to_string(index=False))

#Find the percentage of sales per store

total_sales_per_store = df_period.groupby(['store_number', 'store_name'])[['sale_dollars', 'bottles_sold']].sum().reset_index()

total_sales_per_store.info()


total_sales_per_store['sales_percentage'] = total_sales_per_store['sale_dollars'] / total_sales_per_store['sale_dollars'].sum()
total_sales_per_store['sales_percentage'] *= 100  # Multiply by 100 to get the percentage
total_sales_per_store = total_sales_per_store.sort_values('sales_percentage', ascending=False)
total_sales_per_store['sales_percentage'] = total_sales_per_store['sales_percentage'].map("{:.2f}%".format)

total_sales_per_store.info()


# Use Matplotlib with the newly saved scv and present your Data

totals= total_sales_per_store.merge(df_period[['store_number','zip_code']], on='store_number')

totals.info()

zip_codes = totals['zip_code']
bottles_sold =totals['bottles_sold']

totals['sales_percentage'] = totals['sales_percentage'].str.rstrip('%').astype(float) / 100 # rstrip('%'), the '%' character is removed from each value,
                                                                                            # resulting in a string like '20.54'. Then, the astype(float)
                                                                                            # function is used to convert these strings
                                                                                            # to floating-point numbers.
sale_dollars = totals['sales_percentage']


plt.figure(figsize = (10,6))
plt.scatter(zip_codes, bottles_sold, c = sale_dollars, cmap='Set1_r')
plt.xlabel('Zip Code')
plt.ylabel('Bottles Sold')
plt.title('Total Amount of Bottles Sold per Zip Code\nColorscaling: $ Sales')
plt.colorbar(label = 'Sales Percentage per Store')
plt.show()








