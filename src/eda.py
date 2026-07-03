import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("data/cleaned_business_data.csv")

# Rename columns
df.rename(columns={
    "Rating (fill manually)": "Rating",
    "Reviews (fill manually)": "Reviews"
}, inplace=True)

# Create charts folder if it doesn't exist
os.makedirs("reports/charts", exist_ok=True)

# ----------------------------
# Basic Information
# ----------------------------
print("=" * 50)
print("Dataset Shape")
print(df.shape)

print("\n" + "=" * 50)
print("Columns")
print(df.columns)

print("\n" + "=" * 50)
print("Missing Values")
print(df.isnull().sum())

print("\n" + "=" * 50)
print("Summary Statistics")
print(df[["Rating", "Reviews"]].describe())

print("\n" + "=" * 50)
print("Website Distribution")
print(df["Has Website"].value_counts())

print("\n" + "=" * 50)
print("Top Categories")
print(df["Category"].value_counts())

print("\n" + "=" * 50)
print("Average Rating by Category")
print(
    df.groupby("Category")["Rating"]
      .mean()
      .sort_values(ascending=False)
)

print("\n" + "=" * 50)
print("Top 10 Businesses by Reviews")
print(
    df.sort_values(by="Reviews", ascending=False)
      [["Shop Name", "Category", "Reviews"]]
      .head(10)
)

# ----------------------------
# Chart 1: Website Distribution
# ----------------------------
plt.figure(figsize=(6, 6))
df["Has Website"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%"
)
plt.title("Website Availability")
plt.ylabel("")
plt.tight_layout()
plt.savefig("reports/charts/website_distribution.png")
plt.show()

# ----------------------------
# Chart 2: Top Categories
# ----------------------------
plt.figure(figsize=(10, 6))
sns.countplot(
    y="Category",
    data=df,
    order=df["Category"].value_counts().index
)
plt.title("Business Categories")
plt.xlabel("Count")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig("reports/charts/top_categories.png")
plt.show()

# ----------------------------
# Chart 3: Rating Distribution
# ----------------------------
plt.figure(figsize=(8, 5))
sns.histplot(df["Rating"], bins=10, kde=True)
plt.title("Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("reports/charts/rating_distribution.png")
plt.show()

# ----------------------------
# Chart 4: Top 10 Businesses by Reviews
# ----------------------------
top_reviews = df.sort_values(
    by="Reviews",
    ascending=False
).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_reviews,
    x="Reviews",
    y="Shop Name"
)
plt.title("Top 10 Businesses by Reviews")
plt.tight_layout()
plt.savefig("reports/charts/top_reviews.png")
plt.show()

print("\n" + "=" * 50)
print("EDA Completed Successfully!")
print("Charts saved in reports/charts/")
print("=" * 50)