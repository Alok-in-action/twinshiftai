from typing import Any, Dict, List
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

class PhysicsResidualModel:
    def __init__(self) -> None:
        self.model = RandomForestRegressor(n_estimators=10, random_state=42)
        self.is_calibrated = False

    def fit(self, X: Any, y_residual: Any) -> None:
        self.model.fit(X, y_residual)
        self.is_calibrated = True

    def predict_hybrid(self, y_phys: Any, X: Any) -> Dict[str, Any]:
        if not self.is_calibrated:
            return {"y_hybrid": y_phys, "is_calibrated": False}
        y_res_pred = self.model.predict(X)
        return {
            "y_hybrid": y_phys + y_res_pred,
            "is_calibrated": True
        }

class FailureModeClassifier:
    def __init__(self) -> None:
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        self.is_calibrated = False

    def fit(self, X: Any, y: Any) -> None:
        self.model.fit(X, y)
        self.is_calibrated = True

    def predict_failure_mode(self, X: Any) -> List[Dict[str, Any]]:
        if not self.is_calibrated:
            return [{"predicted_label": "UNKNOWN", "confidence": 0.0} for _ in range(len(X))]
            
        preds = self.model.predict(X)
        probs = self.model.predict_proba(X)
        classes = self.model.classes_
        
        results = []
        for i, pred in enumerate(preds):
            class_idx = list(classes).index(pred)
            conf = probs[i][class_idx]
            results.append({"predicted_label": pred, "confidence": float(conf)})
            
        return results
