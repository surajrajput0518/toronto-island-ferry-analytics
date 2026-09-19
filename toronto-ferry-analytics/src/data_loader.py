import os
import pandas as pd
import numpy as np

def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

def preprocess_and_cache_data(raw_csv_path, parquet_path):
    print(f"Reading raw data from {raw_csv_path}...")
    df = pd.read_csv(raw_csv_path)
    
    # Rename columns cleanly
    rename_dict = {
        "_id": "id",
        "Timestamp": "timestamp",
        "Redemption Count": "redemptions",
        "Sales Count": "sales"
    }
    df = df.rename(columns=rename_dict)
    
    # Clean counts
    df["sales"] = pd.to_numeric(df["sales"], errors="coerce").fillna(0).astype(int)
    df["redemptions"] = pd.to_numeric(df["redemptions"], errors="coerce").fillna(0).astype(int)
    
    # Parse timestamps and sort ascending chronologically
    print("Parsing timestamps and sorting ascending...")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    
    # Operational metrics
    df["net_movement"] = df["sales"] - df["redemptions"]
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["day_name"] = df["timestamp"].dt.day_name()
    df["month"] = df["timestamp"].dt.month
    df["month_name"] = df["timestamp"].dt.month_name()
    df["year"] = df["timestamp"].dt.year
    df["date"] = df["timestamp"].dt.date
    df["is_weekend"] = df["day_of_week"].isin([5, 6])
    df["season"] = df["month"].map(get_season)
    
    # Cyclical trigonometric features for periodic diurnal and annual cycles
    df["sin_hour"] = np.sin(2 * np.pi * df["hour"] / 24.0)
    df["cos_hour"] = np.cos(2 * np.pi * df["hour"] / 24.0)
    df["sin_month"] = np.sin(2 * np.pi * df["month"] / 12.0)
    df["cos_month"] = np.cos(2 * np.pi * df["month"] / 12.0)
    
    # Rolling moving averages
    df["rolling_1h_sales"] = df["sales"].rolling(window=4, min_periods=1).mean().round(1)
    df["rolling_1h_redemptions"] = df["redemptions"].rolling(window=4, min_periods=1).mean().round(1)
    df["rolling_4h_redemptions"] = df["redemptions"].rolling(window=16, min_periods=1).mean().round(1)
    
    # Save optimized parquet
    print(f"Saving preprocessed parquet to {parquet_path}...")
    df.to_parquet(parquet_path, index=False, compression="snappy")
    print(f"Data preprocessed successfully. Total records: {len(df)}")
    return df

def load_data(data_dir=None):
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    
    parquet_path = os.path.join(data_dir, "ferry_tickets_clean.parquet")
    csv_path = os.path.join(data_dir, "ferry_tickets.csv")
    
    if os.path.exists(parquet_path):
        return pd.read_parquet(parquet_path)
    elif os.path.exists(csv_path):
        return preprocess_and_cache_data(csv_path, parquet_path)
    else:
        raise FileNotFoundError(f"Neither {parquet_path} nor {csv_path} was found in {data_dir}.")
