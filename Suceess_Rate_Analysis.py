
import pandas as pd
import numpy as np



df_product = pd.read_csv("zepto_products.csv")
df_sales = pd.read_csv("zepto_sales_cleaned.csv")

df_merge = pd.merge(df_product,df_sales,on=["product_id"],how="left")


#delivery success rate 
#success vs faliure anlysis

status_anyalysis = df_merge.groupby("city")["delivery_status"].value_counts(normalize=True).unstack()*100
print(status_anyalysis.round(2))
