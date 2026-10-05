"""
Energy and Steam-Oil Ratio (SOR) KPI Engine.

Definitions:
SOR = Steam_Volume_CWE [m³] / Produced_Oil_Volume [m³]
SEC = Total_Energy [MJ] / Produced_Oil_Volume [m³] (or bbl)
"""


def calculate_sor(total_steam_m3_cwe: float, total_oil_produced_m3: float) -> float:
    """Calculates cumulative Steam-Oil Ratio (m³ CWE / m³ oil)."""
    if total_oil_produced_m3 <= 0:
        return 0.0
    return float(total_steam_m3_cwe / total_oil_produced_m3)

def calculate_energy_kpis(
    total_steam_m3_cwe: float,
    total_oil_produced_m3: float,
    motor_power_kw: float = 30.0,
    production_days: float = 90.0,
    steam_energy_per_m3_mj: float = 2500.0  # ~2.5 GJ/m³ CWE
) -> dict[str, float]:
    """
    Computes cumulative energy metrics:
    - SOR (m³ CWE / m³ oil)
    - Total Steam Energy (MJ)
    - Total Electrical Energy (MJ & kWh)
    - Specific Energy Consumption SEC (MJ/m³ oil & MJ/bbl oil)
    """
    sor = calculate_sor(total_steam_m3_cwe, total_oil_produced_m3)
    
    steam_energy_mj = total_steam_m3_cwe * steam_energy_per_m3_mj
    
    # Motor electrical energy
    elec_kwh = motor_power_kw * (production_days * 24.0)
    elec_energy_mj = elec_kwh * 3.6  # 1 kWh = 3.6 MJ

    total_energy_mj = steam_energy_mj + elec_energy_mj

    sec_mj_m3 = (total_energy_mj / total_oil_produced_m3) if total_oil_produced_m3 > 0 else 0.0
    # 1 m³ = 6.28981 barrels
    sec_mj_bbl = sec_mj_m3 / 6.28981 if total_oil_produced_m3 > 0 else 0.0

    return {
        "sor_m3_m3": float(sor),
        "steam_energy_mj": float(steam_energy_mj),
        "electrical_energy_kwh": float(elec_kwh),
        "electrical_energy_mj": float(elec_energy_mj),
        "total_energy_mj": float(total_energy_mj),
        "sec_mj_m3": float(sec_mj_m3),
        "sec_mj_bbl": float(sec_mj_bbl)
    }
