
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

delivery_summary = df_merge.groupby("city")["delivery_time_mins"].agg(Average_Time = "mean", Middle_value = "median",Fastest ="min",Slowest = "max",Total_orders = "count",Most_common_time =  lambda x :x.mode().iloc[0] if not x.mode().empty else None )
delivery_summary.round(2)
print("City wise delivery performance")
print(delivery_summary)

#calculating on time rate
#clcultaing the percentage of orders deliverd under 15 minutes

delivery_summary["On_Time_Rate%"] = df_merge.groupby("city")["delivery_time_mins"].apply(lambda x : (x<=15).mean()*100)
delivery_summary = delivery_summary.round(2)
print(delivery_summary["On_Time_Rate%"])

#conclusion

delivery_summary = delivery_summary.sort_values(by = "On_Time_Rate%",ascending = False)
print("\n -- Final Performance by Ranking --")
print(delivery_summary[["Average_Time","On_Time_Rate%"]])

#Why the aveage is so high


stas_summary = df_merge.groupby("city")["delivery_time_mins"].agg(Conistency ="std",Tail_Effect = "skew")
print(stas_summary.round(2))

# finding = the skewness(tail effect) is near zero across all cities, indicates noramal distribution  centered around 26 minutes
#analysis  = the high average is'nt caused by a few bad delivers(outliers).insted the entire delivery process is desgined or perfroming at a 26 minute pace
#business impact   = Zepto 10-15 minute goal is stastically unrealistic for the current operation model as it represent the extreme 5% of delivery rather than norm 

#product popularit vs revnenue

print(df_merge.columns)
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

#delivery success rate 
#success vs faliure anlysis

status_anyalysis = df_merge.groupby("city")["delivery_status"].value_counts(normalize=True).unstack()*100
print(status_anyalysis.round(2))
#done data visulisation 

#friction anyalsis does slowness leads to cancellation?

friction_analysis  = df_merge.groupby("delivery_status")["delivery_time_mins"].agg(["mean","std","median"])
print(friction_analysis)