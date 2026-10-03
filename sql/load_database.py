"""
Load cleaned datasets into SQLite database and execute analytical queries.
File: sql/load_database.py
"""

import sqlite3
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DB_PATH = PROJECT_ROOT / "data" / "dhaka_air_quality.db"
SQL_ANALYSIS_PATH = PROJECT_ROOT / "sql" / "analysis.sql"

print(f"Creating / updating analytical database at {DB_PATH}...")
conn = sqlite3.connect(DB_PATH)

# Load CSVs
df_hourly = pd.read_csv(PROCESSED_DIR / "dhaka_pm25_hourly_cleaned.csv")
df_daily = pd.read_csv(PROCESSED_DIR / "dhaka_pm25_daily_cleaned.csv")
df_case = pd.read_csv(PROCESSED_DIR / "case_cams_daily_cleaned.csv")

# Create dimension tables
df_stations = pd.DataFrame([
    {
        "station_id": "us_embassy_dhaka",
        "station_name": "U.S. Embassy Dhaka (Baridhara)",
        "city": "Dhaka",
        "latitude": 23.7979,
        "longitude": 90.4223,
        "operator": "U.S. Department of State / AirNow DOS",
        "station_type": "Diplomatic / Urban Background"
    },
    {
        "station_id": "dhaka_cams_1",
        "station_name": "Dhaka (CAMS-1 Manik Mia Ave)",
        "city": "Dhaka",
        "latitude": 23.7600,
        "longitude": 90.3800,
        "operator": "Bangladesh Department of Environment (DoE)",
        "station_type": "Institutional / Urban Background"
    },
    {
        "station_id": "dhaka_cams_2",
        "station_name": "Dhaka (CAMS-2 Farmgate)",
        "city": "Dhaka",
        "latitude": 23.7570,
        "longitude": 90.3890,
        "operator": "Bangladesh Department of Environment (DoE)",
        "station_type": "Commercial / High Traffic"
    },
    {
        "station_id": "dhaka_cams_3",
        "station_name": "Dhaka (CAMS-3 Darus Salam)",
        "city": "Dhaka",
        "latitude": 23.7850,
        "longitude": 90.3550,
        "operator": "Bangladesh Department of Environment (DoE)",
        "station_type": "Mixed Urban / Industrial Corridor"
    }
])

# Write tables to SQLite
df_hourly.to_sql("fact_air_quality_hourly", conn, if_exists="replace", index=True, index_label="reading_id")
df_daily.to_sql("fact_air_quality_daily", conn, if_exists="replace", index=False)
df_case.to_sql("fact_case_cams_daily", conn, if_exists="replace", index=False)
df_stations.to_sql("dim_stations", conn, if_exists="replace", index=False)

print("Tables written to SQLite database.")

# Verify query execution
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM fact_air_quality_daily WHERE qc_flag = 'VALID_DAY';")
print("Verified valid days in DB:", cursor.fetchone()[0])

cursor.execute("SELECT season, ROUND(AVG(pm25_mean), 2) FROM fact_air_quality_daily WHERE qc_flag = 'VALID_DAY' GROUP BY season ORDER BY AVG(pm25_mean) DESC;")
print("Verified seasonal SQL query output:")
for row in cursor.fetchall():
    print(" ", row)

conn.close()
print("Database loading and verification complete.")
