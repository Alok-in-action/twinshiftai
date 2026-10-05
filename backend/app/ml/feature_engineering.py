import pandas as pd
from typing import List

def build_leakage_safe_features(df: pd.DataFrame, lags: List[int], rolling_windows: List[int]) -> pd.DataFrame:
    df_feat = df.copy()
    
    # We must ensure data is sorted by time to prevent leakage
    if "time_days" in df_feat.columns:
        df_feat = df_feat.sort_values(by=["well_id", "time_days"])
        
    for lag in lags:
        df_feat[f"oil_rate_m3d_lag_{lag}"] = df_feat.groupby("well_id")["oil_rate_m3d"].shift(lag)
        
    for window in rolling_windows:
        # Shift by 1 first so rolling mean only uses PAST data, not current
        shifted = df_feat.groupby("well_id")["oil_rate_m3d"].shift(1)
        df_feat[f"oil_rate_m3d_roll_mean_{window}"] = shifted.groupby(df_feat["well_id"]).rolling(window=window).mean().reset_index(level=0, drop=True)
        
    return df_feat
