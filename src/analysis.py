import pandas as pd

df = pd.read_csv("data/cleaned_business_data.csv")

df.rename(columns={
    "Rating (fill manually)": "Rating",
    "Reviews (fill manually)": "Reviews"
}, inplace=True)

print("Total Businesses :", len(df))
print()

print("Website Distribution")
print(df["Has Website"].value_counts())
print()

print("Top Categories")
print(df["Category"].value_counts().head(10))
print()

print("Average Rating :", round(df["Rating"].mean(), 2))
print("Average Reviews :", round(df["Reviews"].mean(), 2))