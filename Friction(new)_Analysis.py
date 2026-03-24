import pandas as pd
import numpy as np



df_product = pd.read_csv("zepto_products.csv")
df_sales = pd.read_csv("zepto_sales_cleaned.csv")

df_merge = pd.merge(df_product,df_sales,on=["product_id"],how="left")
df_merge["Total_revenue"] = df_merge["quantity"] * df_merge["base_price"]

#friction anyalsis does slowness leads to cancellation?

friction_analysis  = df_merge.groupby("delivery_status")["delivery_time_mins"].agg(["mean","std","median"])
print(friction_analysis)