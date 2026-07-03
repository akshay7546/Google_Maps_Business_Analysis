import pandas as pd

# Load dataset
df = pd.read_csv("data/business_data.csv")

# Check missing values
print(df.isnull().sum())

# Fill missing values
df["Phone"] = df["Phone"].fillna("Not Available")
df["Website"] = df["Website"].fillna("No Website")
df["Street/Area"] = df["Street/Area"].fillna("Unknown")

# Remove duplicate rows
df = df.drop_duplicates()

# Save cleaned dataset
df.to_csv("data/cleaned_business_data.csv", index=False)

print("Data cleaning completed!")
print(df.shape)