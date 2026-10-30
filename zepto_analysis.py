import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("charts", exist_ok=True)

sns.set_theme(style="white")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["axes.titleweight"] = "bold"

dark = "#4B2E83"
light = "#C9B8E8"

# load data
products = pd.read_csv("zepto_products.csv")
sales = pd.read_csv("zepto_sales.csv")

# clean sales data
sales = sales.drop_duplicates()
sales["order_date"] = pd.to_datetime(sales["order_date"])
sales["city"] = sales["city"].fillna("Unknown")
sales["delivery_status"] = sales["delivery_status"].fillna("Unknown")

city_median = sales.groupby("city")["delivery_time_mins"].transform("median")
sales["delivery_time_mins"] = sales["delivery_time_mins"].fillna(city_median)
sales["delivery_time_mins"] = sales["delivery_time_mins"].fillna(sales["delivery_time_mins"].median())

sales.to_csv("zepto_sales_cleaned.csv", index=False)

# merge sales with products
all_orders = products.merge(sales, on="product_id")
all_orders["revenue"] = all_orders["quantity"] * all_orders["base_price"] / 1e6   # revenue in millions

# keep delivered orders only for revenue charts
df = all_orders[(all_orders["delivery_status"] == "Delivered") & (all_orders["city"] != "Unknown")]


# chart 1 - revenue by category
cat = df.groupby("category")["revenue"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 5.5))
bars = plt.barh(cat.index, cat.values, color=[dark] + [light] * (len(cat) - 1))
plt.bar_label(bars, fmt="%.1fM", padding=5, fontweight="bold")
plt.gca().invert_yaxis()
plt.title("Total Revenue by Product Category (INR)", fontsize=15, loc="left", pad=15)
plt.xticks([])
sns.despine(bottom=True)
plt.tight_layout()
plt.savefig("charts/1_category_revenue.png", dpi=200)
plt.show()


# chart 2 - revenue by city
city = df.groupby("city")["revenue"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 5.5))
bars = plt.bar(city.index, city.values, color=[dark] + [light] * (len(city) - 1))
plt.bar_label(bars, fmt="%.1fM", padding=5, fontweight="bold")
plt.title("Total Revenue by City (INR)", fontsize=15, loc="left", pad=15)
plt.yticks([])
sns.despine(left=True)
plt.tight_layout()
plt.savefig("charts/2_city_revenue.png", dpi=200)
plt.show()


# chart 3 - revenue by city and category
heat = df.pivot_table(index="city", columns="category", values="revenue", aggfunc="sum")
heat = heat.loc[city.index, cat.index]

plt.figure(figsize=(11, 6))
sns.heatmap(heat, annot=True, fmt=".1f", cmap="Purples", linewidths=1,
            cbar=False, annot_kws={"fontweight": "bold"})
plt.title("Revenue by City and Category (INR Millions)", fontsize=15, loc="left", pad=15)
plt.xlabel("")
plt.ylabel("")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/3_city_category_heatmap.png", dpi=200)
plt.show()


# chart 4 - order status split
status = all_orders[all_orders["delivery_status"] != "Unknown"]
status = status["delivery_status"].value_counts(normalize=True) * 100

plt.figure(figsize=(10, 4.5))
bars = plt.barh(status.index, status.values, color=[dark] + [light] * (len(status) - 1))
plt.bar_label(bars, fmt="%.1f%%", padding=5, fontweight="bold")
plt.gca().invert_yaxis()
plt.title("Order Outcome: Delivered, Cancelled and Returned (%)", fontsize=15, loc="left", pad=15)
plt.xticks([])
sns.despine(bottom=True)
plt.tight_layout()
plt.savefig("charts/4_order_status_split.png", dpi=200)
plt.show()


# chart 5 - top 10 products
top = df.groupby("product_name")["revenue"].sum().nlargest(10)

plt.figure(figsize=(10, 6))
bars = plt.barh(top.index, top.values, color=[dark] + [light] * 9)
plt.bar_label(bars, fmt="%.1fM", padding=5, fontweight="bold")
plt.gca().invert_yaxis()
plt.title("Top 10 Products by Revenue (INR)", fontsize=15, loc="left", pad=15)
plt.xticks([])
sns.despine(bottom=True)
plt.tight_layout()
plt.savefig("charts/5_top_10_products.png", dpi=200)
plt.show()