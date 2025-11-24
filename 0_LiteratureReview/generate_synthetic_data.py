#!/usr/bin/env python3
"""
Generate synthetic hourly data for testing the baseline pipeline.
Writes 0_LiteratureReview/feature_template.csv with realistic-ish patterns.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import os

SCRIPT_DIR = Path(__file__).resolve().parent
OUT_CSV = SCRIPT_DIR / "feature_template.csv"

def generate(start="2024-01-01", periods=24*365, seed=42):
    rng = pd.date_range(start=start, periods=periods, freq="h")
    np.random.seed(seed)
    hour = rng.hour
    dayofweek = rng.dayofweek
    # Base load with daily and weekly seasonality
    base_load = 50000 + 8000 * np.sin(2 * np.pi * hour / 24) + 3000 * (dayofweek >= 5)
    noise = np.random.normal(0, 1000, size=periods)
    load = base_load + noise
    # Renewable generation (PV daytime, wind random)
    irradiance = np.clip(1000 * np.maximum(0, np.sin((hour - 6) / 24 * 2 * np.pi)), 0, None) + np.random.normal(0, 50, periods)
    pv_gen = np.clip(2000 * (irradiance / 1000) + np.random.normal(0, 100, periods), 0, None)
    wind_gen = np.clip(1500 + 500 * np.sin(np.linspace(0, 20*np.pi, periods)) + np.random.normal(0, 200, periods), 0, None)
    temp = 10 + 8 * np.sin(2 * np.pi * (rng.dayofyear) / 365) + np.random.normal(0, 3, periods)
    humidity = np.clip(60 + 20 * np.sin(2 * np.pi * hour / 24) + np.random.normal(0, 5, periods), 0, 100)
    # Price: base + sensitivity to net load
    net_load = load - (pv_gen + wind_gen)
    price = 30 + 0.0005 * net_load + 5 * np.sin(2 * np.pi * hour / 24) + np.random.normal(0, 3, periods)
    df = pd.DataFrame({
        "timestamp": rng,
        "price": price.round(2),
        "load": load.round(1),
        "pv_gen": pv_gen.round(1),
        "wind_gen": wind_gen.round(1),
        "temp": temp.round(2),
        "humidity": humidity.round(1),
        "irradiance": irradiance.round(1),
        "hour": hour,
        "day_of_week": dayofweek,
        "is_holiday": 0,
    })
    # add simple lag columns for convenience
    df["lag_price_1h"] = df["price"].shift(1).bfill()
    df["lag_price_24h"] = df["price"].shift(24).bfill()
    df["lag_load_1h"] = df["load"].shift(1).bfill()
    df["lag_load_24h"] = df["load"].shift(24).bfill()
    df["rolling_mean_load_24h"] = df["load"].rolling(24, min_periods=1).mean()
    df["rolling_std_load_24h"] = df["load"].rolling(24, min_periods=1).std().fillna(0)
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)
    print(f"Wrote synthetic CSV to {OUT_CSV} with {len(df)} rows")

if __name__ == "__main__":
    generate()
