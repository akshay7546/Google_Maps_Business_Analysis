import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/cleaned_business_data.csv")

# Rename columns
df.rename(columns={
    "Rating (fill manually)": "Rating",
    "Reviews (fill manually)": "Reviews"
}, inplace=True)

# 1. Website Distribution Pie Chart
plt.figure(figsize=(6, 6))
df["Has Website"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%"
)
plt.title("Website vs No Website")
plt.ylabel("")
plt.savefig("reports/charts/website_distribution.png")
plt.show()

# 2. Top Categories
plt.figure(figsize=(10, 6))
df["Category"].value_counts().head(10).plot(kind="bar")
plt.title("Top 10 Business Categories")
plt.xlabel("Category")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/charts/top_categories.png")
plt.show()

# 3. Rating Distribution
plt.figure(figsize=(8, 5))
df["Rating"].hist(bins=10)
plt.title("Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("reports/charts/rating_distribution.png")
plt.show()

print("Charts created successfully!")