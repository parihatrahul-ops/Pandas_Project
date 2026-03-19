import pandas as pd

df = pd.read_csv("zepto_products.csv")

#information about the dataset

print(df.shape)
print(df.columns)
print(df.info())
print(df)

#no null vlaues 



print(df.groupby(["category","product_name"])["base_price"].sum())
print(df)