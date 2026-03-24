import pandas as pd
import numpy as np



df_product = pd.read_csv("zepto_products.csv")
df_sales = pd.read_csv("zepto_sales_cleaned.csv")

df_merge = pd.merge(df_product,df_sales,on=["product_id"],how="left")
data_array  = df_merge.to_numpy()

df_merge["Total_revenue"] = df_merge["quantity"] * df_merge["base_price"]

#product popularity vs revnenue

product_analysis = df_merge.groupby("product_name").agg(Popularity_count = ("order_id","count"), Total_Earnings = ("Total_revenue","sum"))

#sorting the products to check most profitable product first

product_analysis= product_analysis.sort_values(by="Total_Earnings",ascending=False)
print("\n -- Product anyalsis leaderboard")
print(product_analysis.head(10))


#Average order Value to indentify which prodcut are perimum earner vs voulme earners
#calculte how much each product earns on each order

product_analysis["Avg_order_value"] = product_analysis["Total_Earnings"]/product_analysis["Popularity_count"]

#sort

Premimum_products = product_analysis.sort_values(by = "Avg_order_value",ascending=False)
print("\n Top 10 High value Premimum Products")
print(Premimum_products[["Avg_order_value","Total_Earnings"]].head(10))
