# fleet_cleaner.py

import pandas as pd

# Step 1: Load CSV file
file_path = r"C:\Users\koush\OneDrive\Desktop\project 2\fleet_data.csv"
 # Change this to your CSV file path
df = pd.read_csv(file_path)

# Step 2: Basic Inspection
print("First 5 rows:\n", df.head())
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())

# Step 3: Clean Column Names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")

# Step 4: Handle Missing Values
# Drop rows with more than 50% missing values
df = df.dropna(thresh=len(df.columns) // 2)

# Fill missing numeric columns with their mean (if exists)
numeric_cols = df.select_dtypes(include='number').columns
for col in numeric_cols:
    df[col].fillna(df[col].mean(), inplace=True)

# Step 5: Convert Date Columns
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Fix invalid dates

# Step 6: Convert mileage and fuel columns to numeric (if not already)
if 'mileage' in df.columns:
    df['mileage'] = pd.to_numeric(df['mileage'], errors='coerce')

if 'fuel_consumed' in df.columns:
    df['fuel_consumed'] = pd.to_numeric(df['fuel_consumed'], errors='coerce')

# Step 7: Remove Duplicates
df.drop_duplicates(inplace=True)

# Step 8: Filter Outliers (example: unrealistic mileage > 1 million)
if 'mileage' in df.columns:
    df = df[df['mileage'] < 1_000_000]

# Step 9: Final Check
print("\nCleaned Data Sample:\n", df.head())
print("\nCleaned Data Info:\n")
df.info()

# Step 10: Save Cleaned Data
df.to_csv("fleet_data_cleaned.csv", index=False)
print("\n✅ Cleaned data saved to fleet_data_cleaned.csv")
