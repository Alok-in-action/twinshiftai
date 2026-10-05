import pandas as pd
from typing import Tuple, Any, Dict

def split_chronological(df: pd.DataFrame, train_ratio: float = 0.7) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if "time_days" in df.columns:
        df = df.sort_values(by=["well_id", "time_days"])
        
    split_idx = int(len(df) * train_ratio)
    return df.iloc[:split_idx].copy(), df.iloc[split_idx:].copy()

def split_by_css_cycle(df: pd.DataFrame, test_cycle_id: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_df = df[df["cycle_id"] != test_cycle_id].copy()
    test_df = df[df["cycle_id"] == test_cycle_id].copy()
    return train_df, test_df

def split_by_well(df: pd.DataFrame, test_well_id: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_df = df[df["well_id"] != test_well_id].copy()
    test_df = df[df["well_id"] == test_well_id].copy()
    return train_df, test_df

class MLflowTracker:
    def __init__(self, experiment_name: str) -> None:
        self.experiment_name = experiment_name

    def log_params(self, params: Dict[str, Any]) -> None:
        pass # Stub fallback if mlflow not present

    def log_metrics(self, metrics: Dict[str, float]) -> None:
        pass # Stub fallback if mlflow not present
