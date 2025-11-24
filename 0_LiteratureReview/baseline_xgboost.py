#!/usr/bin/env python3
"""
Baseline XGBoost example for a price/load forecasting target.
Reads `0_LiteratureReview/feature_template.csv`, trains an XGBoost regressor
with rolling (time-series) cross-validation when data is sufficient, and reports MAE/RMSE.
Saves final model to `0_LiteratureReview/baseline_model.pkl`.
"""
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor
import joblib
import sys
import math

INPUT_CSV = os.path.join("0_LiteratureReview", "feature_template.csv")
MODEL_OUT = os.path.join("0_LiteratureReview", "baseline_model.pkl")

def load_data(path):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").set_index("timestamp")
    return df

def prepare_features(df, target_shift=1):
    df = df.copy()
    df["target"] = df["price"].shift(-target_shift)
    df = df.dropna(subset=["target"])
    exclude = {"target"}
    features = [c for c in df.columns if c not in exclude]
    features = [c for c in features if pd.api.types.is_numeric_dtype(df[c])]
    X = df[features].ffill().bfill().fillna(0)
    y = df["target"].values
    return X, y

def rolling_cv_evaluate(X, y, n_splits=5):
    n_samples = X.shape[0]
    if n_samples <= n_splits:
        print(f"Not enough samples ({n_samples}) for TimeSeriesSplit(n_splits={n_splits}). Skipping CV.")
        return None
    tscv = TimeSeriesSplit(n_splits=n_splits)
    maes = []
    rmses = []
    fold = 0
    for train_idx, test_idx in tscv.split(X):
        fold += 1
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        model = XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, verbosity=0)
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, pred)
        mse = mean_squared_error(y_test, pred)
        rmse = math.sqrt(mse)
        maes.append(mae)
        rmses.append(rmse)
        print(f"Fold {fold}: MAE={mae:.4f}, RMSE={rmse:.4f}")
    if maes:
        print(f"CV Mean MAE: {np.mean(maes):.4f}  RMSE: {np.mean(rmses):.4f}")
    return model

def train_final_model(X, y):
    model = XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.05, random_state=42, verbosity=0)
    model.fit(X, y)
    return model

def main():
    if not os.path.exists(INPUT_CSV):
        raise FileNotFoundError(f"Input CSV not found: {INPUT_CSV}")
    df = load_data(INPUT_CSV)
    X, y = prepare_features(df, target_shift=1)
    print(f"Data loaded: X shape {X.shape}, y length {len(y)}")
    if len(y) == 0:
        print("No training samples available after target shift. Exiting.")
        sys.exit(1)
    print("Running rolling CV evaluation (if sufficient data)...")
    _ = rolling_cv_evaluate(X, y, n_splits=5)
    print("Training final model on full dataset...")
    final_model = train_final_model(X, y)
    joblib.dump({"model": final_model, "features": X.columns.tolist()}, MODEL_OUT)
    print(f"Model saved to {MODEL_OUT}")

if __name__ == "__main__":
    main()
