from typing import Dict, Any
from backend.app.schemas.dynamometer import DiagnosticMetrics, EquipmentLimitsConfig

class OptimizationSafetyValidator:
    def __init__(self, limits: EquipmentLimitsConfig = EquipmentLimitsConfig()) -> None:
        self.limits = limits

    def validate_scenario_metrics(self, metrics: DiagnosticMetrics, max_allowed_temp_c: float = 250.0, simulated_temp_c: float = 0.0) -> Dict[str, Any]:
        violations = []
        
        if metrics.pprl_lbs > self.limits.max_pprl_lbs:
            violations.append(f"PPRL {metrics.pprl_lbs} exceeds limit {self.limits.max_pprl_lbs}")
            
        if metrics.peak_gearbox_torque_in_lbs > self.limits.max_gearbox_torque_in_lbs:
            violations.append(f"Gearbox Torque {metrics.peak_gearbox_torque_in_lbs} exceeds limit {self.limits.max_gearbox_torque_in_lbs}")
            
        if metrics.rod_floating_margin_lbs < self.limits.min_rod_floating_margin_lbs:
            violations.append(f"Rod floating margin {metrics.rod_floating_margin_lbs} below minimum {self.limits.min_rod_floating_margin_lbs}")
            
        if simulated_temp_c > max_allowed_temp_c:
            violations.append(f"Simulated temperature {simulated_temp_c} exceeds allowed {max_allowed_temp_c}")

        is_safe = len(violations) == 0
        return {
            "is_safe": is_safe,
            "blocked_from_recommendation": not is_safe,
            "violations": violations
        }
