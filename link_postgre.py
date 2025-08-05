import psycopg2
import pandas as pd
import os

# Step 1: Read the cleaned CSV
file_path = r"C:\Users\koush\OneDrive\Desktop\project 2\fleet_data_cleaned.csv"

if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    print("Please verify:")
    print("1. The file exists at this location")
    print("2. The file name is exactly 'fleet_data_cleaned.csv'")
    exit()

try:
    df = pd.read_csv(file_path)
    print("CSV loaded successfully. Columns:", df.columns.tolist())
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

# Step 2: PostgreSQL connection
try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="vehicles",
        user="postgres",
        password="1234"
    )
    cur = conn.cursor()
    
    # Create table (modify to match your columns)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS fleet (
        trip_id VARCHAR PRIMARY KEY,
        vehicle_id VARCHAR,
        date DATE,
        distance_km FLOAT,
        fuel_liters FLOAT,
        avg_speed_kmph FLOAT
    );
    """)
    
    # Insert data
    for index, row in df.iterrows():
        cur.execute("""
            INSERT INTO fleet (trip_id, vehicle_id, date, distance_km, fuel_liters, avg_speed_kmph)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            row['trip_id'],
            row['vehicle_id'],
            row['date'],
            row['distance_km'],
            row['fuel_liters'],
            row['avg_speed_kmph']
        ))
    
    conn.commit()
    print("Data successfully imported to PostgreSQL 🚀")

except Exception as e:
    print(f"Database error: {e}")
    if 'conn' in locals():
        conn.rollback()
finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()