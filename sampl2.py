
import pandas as pd
import numpy as np



df_product = pd.read_csv("zepto_products.csv")
df_sales = pd.read_csv("zepto_sales_cleaned.csv")

df_merge = pd.merge(df_product,df_sales,on=["product_id"],how="left")
data_array  = df_merge.to_numpy()


# print(df_merge.info())
# print(df_merge.columns)
# print(df_merge.info())
# print(df_merge.describe())

#calculating the total revenue


df_merge["Total_revenue"] = df_merge["quantity"] * df_merge["base_price"]
# print(df_merge["Total_revenue"])
print(df_merge)

#GROUPING BY CATEGORY WHICH BRINGING THE MOST MONEY
#matplotlib chart 

category_revenue = df_merge.groupby("category")["Total_revenue"].sum().sort_values(ascending=False)
print("Top 5 Category by revenue:")
print(category_revenue.head())

#market performance by city
# print(df_merge.columns)

city_revnue = df_merge.groupby("city")["Total_revenue"].sum().sort_values(ascending = False)
print(city_revnue.head())

#Delivery performance of zepto
#since zepto claims delivery under 10 minutes we categorized delivery under 15 minutes is on time

delivery_performance = df_merge.groupby("city")["delivery_time_mins"].agg(["mean",""])
print(df_merge.columns)





