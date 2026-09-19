import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score

class FerryDemandForecaster:
    def __init__(self):
        self.model = Ridge(alpha=1.0)
        self.feature_cols = [
            "sin_hour", "cos_hour", "sin_month", "cos_month",
            "is_weekend", "day_of_week",
            "lag_1", "lag_4", "lag_96", "rolling_4h"
        ]
        self.is_trained = False
        
    def prepare_features(self, df):
        sub = df[["timestamp", "redemptions", "sin_hour", "cos_hour", "sin_month", "cos_month", "is_weekend", "day_of_week"]].copy()
        sub["lag_1"] = sub["redemptions"].shift(1)
        sub["lag_4"] = sub["redemptions"].shift(4)
        sub["lag_96"] = sub["redemptions"].shift(96)
        sub["rolling_4h"] = sub["redemptions"].rolling(16, min_periods=1).mean()
        sub = sub.dropna().reset_index(drop=True)
        return sub

    def train_quick_model(self, df, sample_size=40000):
        prep = self.prepare_features(df)
        if len(prep) > sample_size:
            prep = prep.iloc[-sample_size:].reset_index(drop=True)
            
        X = prep[self.feature_cols]
        y = prep["redemptions"]
        
        split = int(len(prep) * 0.8)
        X_train, X_test = X.iloc[:split], X.iloc[split:]
        y_train, y_test = y.iloc[:split], y.iloc[split:]
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        y_pred = self.model.predict(X_test)
        y_pred = np.maximum(0, y_pred)
        
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        return {
            "mae": round(mae, 2),
            "r2": round(r2, 3),
            "test_y": y_test.values[-96:],
            "pred_y": y_pred[-96:],
            "timestamps": prep["timestamp"].iloc[split:].values[-96:]
        }

    def forecast_upcoming(self, df, steps=96):
        # Forecast the next 24 hours (96 intervals of 15m)
        if not self.is_trained:
            self.train_quick_model(df)
            
        prep = self.prepare_features(df)
        last_rows = prep.iloc[-1:].copy()
        
        preds = []
        cur_row = last_rows.iloc[0].to_dict()
        last_ts = cur_row["timestamp"]
        
        lag_buffer = list(prep["redemptions"].iloc[-100:].values)
        
        future_ts = [last_ts + pd.Timedelta(minutes=15 * (i + 1)) for i in range(steps)]
        
        for i in range(steps):
            ts = future_ts[i]
            h = ts.hour
            m = ts.month
            dow = ts.dayofweek
            is_wknd = dow in [5, 6]
            
            f_vec = [
                np.sin(2 * np.pi * h / 24.0),
                np.cos(2 * np.pi * h / 24.0),
                np.sin(2 * np.pi * m / 12.0),
                np.cos(2 * np.pi * m / 12.0),
                1.0 if is_wknd else 0.0,
                dow,
                lag_buffer[-1],
                lag_buffer[-4] if len(lag_buffer) >= 4 else lag_buffer[-1],
                lag_buffer[-96] if len(lag_buffer) >= 96 else lag_buffer[-1],
                np.mean(lag_buffer[-16:])
            ]
            
            p = max(0.0, float(self.model.predict([f_vec])[0]))
            preds.append(p)
            lag_buffer.append(p)
            
        return pd.DataFrame({
            "timestamp": future_ts,
            "forecasted_redemptions": [round(x) for x in preds],
            "lower_bound": [max(0, round(x * 0.85)) for x in preds],
            "upper_bound": [round(x * 1.15) for x in preds]
        })
