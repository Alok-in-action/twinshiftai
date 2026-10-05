# Equations

## 1. CSS Thermal State
**Reduced-order thermal balance:**
```math
C_{\mathrm{eff}}\frac{dT_h}{dt} = \dot Q_{\mathrm{steam}} - U A (T_h-T_{\mathrm{far}}) - \dot m_{\mathrm{prod}} c_p (T_h-T_{\mathrm{ref}})
```
- Variables: $T_h$ (heated-zone temperature, K), $p_r$ (reservoir pressure, Pa).
- Assumption: Lumped or reduced radial thermal gradient.

## 2. Fluid Properties
**Andrade Viscosity Equation:**
```math
\ln \mu_o = A + \frac{B}{T}
```
- Variables: $\mu_o$ (oil viscosity), $T$ (temperature, K).
- Note: Do not extrapolate beyond measured temperatures.

## 3. Reservoir Inflow
**Radial Darcy-type Inflow:**
```math
q_o = \frac{2\pi k h}{\mu_o(T) B_o} \frac{p_r-p_{wf}}{\ln(r_e/r_w)+s}
```
- Variables: $q_o$ (oil flow rate), $k$ (permeability), $h$ (thickness), $\mu_o(T)$ (temperature-dependent viscosity), $p_r$ (reservoir pressure), $p_{wf}$ (bottomhole flowing pressure).

## 4. SRP Kinematics
**Sinusoidal Approximation:**
```math
x_s(t)=\frac{S}{2}\left[1-\cos(\omega t)\right], \quad v_s(t)=\frac{S\omega}{2}\sin(\omega t)
```
- Variables: $x_s$ (polished rod position), $v_s$ (velocity), $S$ (stroke length), $\omega$ (angular velocity).

## 5. Rod-String Dynamics
**Damped Wave Equation:**
```math
\rho_r A_r \frac{\partial^2 u}{\partial t^2} = E A_r \frac{\partial^2 u}{\partial z^2} - c(z,T,\mu)\frac{\partial u}{\partial t} + f_g + f_b + f_f
```
- Variables: $u$ (displacement), $z$ (depth), $t$ (time), $\rho_r$ (rod density), $A_r$ (cross-sectional area).

## 6. Pump Displacement
```math
q_{\mathrm{theoretical}} = A_p S_p N C_t
```
```math
q_l = q_{\mathrm{theoretical}}\eta_v
```

## 7. Rod Floating Margin
```math
M_{\mathrm{float}} = F_{\mathrm{down,available}} - F_{\mathrm{up,resisting}}
```

## 8. Energy KPIs
```math
SOR = \frac{V_{\mathrm{steam,cold\ water\ equivalent}}}{V_{\mathrm{oil}}}
```
```math
SEC = \frac{E_{\mathrm{steam}}+E_{\mathrm{electric}}}{V_{\mathrm{oil}}}
```
