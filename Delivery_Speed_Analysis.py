import pandas as pd
import numpy as np



df_product = pd.read_csv("zepto_products.csv")
df_sales = pd.read_csv("zepto_sales_cleaned.csv")

df_merge = pd.merge(df_product,df_sales,on=["product_id"],how="left")
data_array  = df_merge.to_numpy()



#Delivery performance of zepto
#since zepto claims delivery under 10 -15 minutes we categorized delivery under 15 minutes is on time

delivery_summary = df_merge.groupby("city")["delivery_time_mins"].agg(Average_Time = "mean", Middle_value = "median",Fastest ="min",Slowest = "max",Total_orders = "count",Most_common_time =  lambda x :x.mode().iloc[0] if not x.mode().empty else None )
delivery_summary.round(2)
print("\n -- City wise delivery performance")
print(delivery_summary)


#calculating on time rate
#clcultaing the percentage of orders deliverd under 15 minutes

delivery_summary["On_Time_Rate%"] = df_merge.groupby("city")["delivery_time_mins"].apply(lambda x : (x<=15).mean()*100)
delivery_summary = delivery_summary.round(2)
print(" \n -- Delivery_summarry which are on time")
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

