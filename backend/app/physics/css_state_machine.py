"""
CSS State Machine.

Phases:
1. INJECTION: High-pressure steam injection into reservoir.
2. SOAK: Well shut-in to allow heat transfer into heavy crude.
3. PRODUCTION: Well put on SRP lift; oil & water produced while reservoir cools.
4. CUTOFF: Economic/thermal limit reached; well shut-in or prepped for next cycle.
"""

from enum import Enum


class CSSPhase(str, Enum):
    INJECTION = "injection"
    SOAK = "soak"
    PRODUCTION = "production"
    CUTOFF = "cutoff"

class CSSStateMachine:
    """Manages cycle state transitions and elapsed durations."""

    def __init__(
        self,
        injection_duration_days: float = 10.0,
        soak_duration_days: float = 5.0,
        production_duration_days: float = 90.0,
        min_economic_oil_rate_m3d: float = 0.5
    ):
        self.inj_days = injection_duration_days
        self.soak_days = soak_duration_days
        self.prod_days = production_duration_days
        self.min_oil_rate = min_economic_oil_rate_m3d

    def get_phase_at_time(self, elapsed_days: float, current_oil_rate_m3d: float = 10.0) -> CSSPhase:
        """Determines the current CSS phase given elapsed time from injection start in days."""
        if elapsed_days < 0:
            raise ValueError("Elapsed time cannot be negative")

        if elapsed_days <= self.inj_days:
            return CSSPhase.INJECTION

        soak_end = self.inj_days + self.soak_days
        if elapsed_days <= soak_end:
            return CSSPhase.SOAK

        prod_end = soak_end + self.prod_days
        if elapsed_days <= prod_end:
            if current_oil_rate_m3d < self.min_oil_rate:
                return CSSPhase.CUTOFF
            return CSSPhase.PRODUCTION

        return CSSPhase.CUTOFF

    def calculate_cycle_durations(self, total_cycle_days: float) -> dict[str, float]:
        """Calculates expected phase breakdown for a given total cycle length."""
        return {
            "injection_days": min(self.inj_days, total_cycle_days),
            "soak_days": max(0.0, min(self.soak_days, total_cycle_days - self.inj_days)),
            "production_days": max(0.0, total_cycle_days - self.inj_days - self.soak_days)
        }
