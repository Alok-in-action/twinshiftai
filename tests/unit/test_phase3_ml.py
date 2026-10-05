"""
Phase 3 Verification Tests: Leakage-Safe Feature Engineering, Physics Residual Model,
Classifier Interfaces, and Out-of-Sample Validation Splits.
"""

import pytest
import pandas as pd
import numpy as np

from backend.app.ml.feature_engineering import build_leakage_safe_features
from backend.app.ml.residual_model import PhysicsResidualModel, FailureModeClassifier
from backend.app.ml.validation import split_chronological, split_by_css_cycle, split_by_well, MLflowTracker

def test_leakage_safe_feature_engineering() -> None:
    data = {
        "well_id": ["BW-01"] * 10,
        "time_days": list(range(10)),
        "oil_rate_m3d": [10.0, 12.0, 15.0, 14.0, 18.0, 20.0, 22.0, 21.0, 19.0, 17.0],
        "temperature_c": [100.0, 95.0, 90.0, 85.0, 80.0, 75.0, 70.0, 65.0, 60.0, 55.0]
    }
    df = pd.DataFrame(data)
    feat_df = build_leakage_safe_features(df, lags=[1, 2], rolling_windows=[3])

    assert "oil_rate_m3d_lag_1" in feat_df.columns
    assert "oil_rate_m3d_roll_mean_3" in feat_df.columns
    assert feat_df.loc[3, "oil_rate_m3d_lag_1"] == 15.0

def test_chronological_and_cycle_splits() -> None:
    data = {
        "well_id": ["BW-01"] * 10,
        "time_days": list(range(10)),
        "cycle_id": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
        "oil_rate_m3d": [10.0] * 10
    }
    df = pd.DataFrame(data)

    train_c, test_c = split_chronological(df, train_ratio=0.7)
    assert len(train_c) == 7
    assert len(test_c) == 3

    train_cycle, test_cycle = split_by_css_cycle(df, test_cycle_id=2)
    assert len(test_cycle) == 5
    assert (test_cycle["cycle_id"] == 2).all()

def test_physics_residual_model() -> None:
    model = PhysicsResidualModel()
    X = np.random.rand(20, 3)
    y_phys = np.ones(20) * 100.0
    y_actual = y_phys + np.sin(np.linspace(0, 3, 20)) * 5.0
    y_residual = y_actual - y_phys

    model.fit(X, y_residual)
    res = model.predict_hybrid(y_phys, X)

    assert res["is_calibrated"]
    assert len(res["y_hybrid"]) == 20

def test_failure_mode_classifier() -> None:
    clf = FailureModeClassifier()
    X = np.random.rand(20, 3)
    labels = ["NORMAL"] * 10 + ["FLUID_POUND"] * 10

    clf.fit(X, labels)
    preds = clf.predict_failure_mode(X[:2])

    assert len(preds) == 2
    assert "predicted_label" in preds[0]
    assert "confidence" in preds[0]
    assert preds[0]["confidence"] > 0.0

def test_mlflow_tracker_fallback() -> None:
    tracker = MLflowTracker("Test_Exp")
    tracker.log_params({"spm": 6.0})
    tracker.log_metrics({"rmse": 1.25})
