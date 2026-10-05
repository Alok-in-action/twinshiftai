# Assumptions

## 1. Physics Model
- **Reservoir Flow**: Reduced radial Darcy inflow is sufficient for the MVP.
- **Thermal Model**: Lumped parameter or simple radial reduced-order model rather than full finite-volume grid. Heat losses to overburden/underburden are approximated via overall heat transfer coefficients.
- **Multiphase Flow**: Homogeneous or no-slip multiphase assumptions applied for initial wellbore traverse; to be refined later if data supports it.
- **SRP Kinematics**: Pure sinusoidal kinematics are assumed as a fallback when actual unit geometry data is absent.
- **Rod Dynamics**: 1D damped wave equation with estimated fluid drag.

## 2. Fluid Properties
- **Viscosity**: Driven purely by temperature using a calibrated Andrade relation or interpolation table. Pressure effects on liquid viscosity are negligible.
- **Steam**: Steam properties strictly follow standard CoolProp tables for pure water/steam.

## 3. Data & ML
- **Data Completeness**: Missing operational bounds will block optimization to maintain safety.
- **ML Independence**: ML residual models assume the physics base model captures the primary phenomenological trends.

## 4. Field Implementation
- **Advisory Role**: The system has no direct capability to change VFD or PLC settings without human transcription.
