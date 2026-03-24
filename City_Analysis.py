import pandas as pd
import numpy as np



df_product = pd.read_csv("zepto_products.csv")
df_sales = pd.read_csv("zepto_sales_cleaned.csv")

df_merge = pd.merge(df_product,df_sales,on=["product_id"],how="left")
data_array  = df_merge.to_numpy()

df_merge["Total_revenue"] = df_merge["quantity"] * df_merge["base_price"]

city_revnue = df_merge.groupby("city")["Total_revenue"].sum().sort_values(ascending = False)
print(city_revnue.head())