import pandas as pd
import numpy as np

def calculate_executive_kpis(df):
    total_sales = int(df["sales"].sum())
    total_redemptions = int(df["redemptions"].sum())
    net_movement = total_sales - total_redemptions
    redemption_rate = (total_redemptions / total_sales * 100) if total_sales > 0 else 0.0
    
    # Peak interval and date
    max_redemption_idx = df["redemptions"].idxmax()
    peak_record = df.loc[max_redemption_idx]
    peak_val = int(peak_record["redemptions"])
    peak_ts = peak_record["timestamp"]
    
    # Average per hour during active hours (08:00 - 22:00)
    active_df = df[df["hour"].between(8, 22)]
    avg_sales_hourly = active_df.groupby(["date", "hour"])["sales"].sum().mean()
    avg_redemptions_hourly = active_df.groupby(["date", "hour"])["redemptions"].sum().mean()
    
    # Seasonal Utilization Index (Winter avg vs Summer avg)
    summer_vol = df[df["season"] == "Summer"]["redemptions"].sum()
    winter_vol = df[df["season"] == "Winter"]["redemptions"].sum()
    summer_intervals = len(df[df["season"] == "Summer"])
    winter_intervals = len(df[df["season"] == "Winter"])
    
    summer_rate = (summer_vol / summer_intervals) if summer_intervals > 0 else 1.0
    winter_rate = (winter_vol / winter_intervals) if winter_intervals > 0 else 0.0
    osui = (winter_rate / summer_rate * 100) if summer_rate > 0 else 0.0
    
    return {
        "total_sales": total_sales,
        "total_redemptions": total_redemptions,
        "net_movement": net_movement,
        "redemption_rate": round(redemption_rate, 2),
        "peak_redemption_interval": peak_val,
        "peak_redemption_timestamp": peak_ts,
        "avg_sales_hourly": round(avg_sales_hourly, 1),
        "avg_redemptions_hourly": round(avg_redemptions_hourly, 1),
        "off_season_utilization_index": round(osui, 2)
    }

def get_peak_windows(df):
    hourly = df.groupby(["day_name", "hour"])[["sales", "redemptions"]].mean().reset_index()
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hourly["day_name"] = pd.Categorical(hourly["day_name"], categories=days_order, ordered=True)
    hourly = hourly.sort_values(["day_name", "hour"])
    return hourly
