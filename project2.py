import pandas as pd
df = pd.read_csv("zepto_sales.csv")

#inforamtion about the dataset

print(df.shape)
print(df.columns)
print(df.info())
print(df.isnull().sum())


#filling the null values
# 1.) city by using forwardfill function

df["city"]=df["city"].ffill()
print(df["city"])
print(df.isnull().sum())

# 2.) delivery_stauts by using forwardfill

print(df["delivery_status"].isnull().sum())
print(["delivery_status"])
df["delivery_status"]= df["delivery_status"].ffill()

# 3.) delivery_time_mins by using interpoltae ,method = time
#     time method uses actual clock time to decide how to fill gap
#     first i converted the order_date to datetime because pandas treat datetime as object
#     second i gave them  index by df.set_index because time method only works if the index of your dataframe is made of dates

df["order_date"]=pd.to_datetime(df["order_date"])
df.set_index("order_date",inplace=True)
df["delivery_time_mins"]= df["delivery_time_mins"].interpolate(method="time")
print(df["delivery_time_mins"].isnull().sum())
print(df["delivery_time_mins"].describe())

#rechecking all the null values are filled or not

print(df.isnull().sum())

#Data frame is now clean
#sroting the data on the basis of product id and order date

print(df.sort_values(by=["product_id","order_date"],ascending=[True,False]))

#using groupby to check the total 38 products
#print(df["product_id"].nunique())
print(df.groupby("product_id")["quantity"].sum())

df.to_csv("zepto_sales_cleaned.csv",index=False)

