# Data Dictionary

| Entity | Description | Core Fields |
|---|---|---|
| `wells` | Static wellbore geometry & metadata | well_id, coordinates, depth, deviation, completion, perforations, tubing geometry, casing geometry |
| `reservoir_properties` | Subsurface definitions | net_pay, porosity, permeability, pressure, temperature, saturations, boundaries |
| `fluid_pvt` | Measured PVT and fluid data | timestamp/sample_id, temperature, pressure, viscosity, density, Bo, water_cut, gas_data |
| `css_cycles` | Phase timings and injected steam specs | well, cycle, injection_start/end, steam_mass/cwe, quality, pressure, temperature, soak_start/end, production_restart/cutoff |
| `production_daily` | Daily measured well output | well, timestamp, oil, water, gas, fluid, hours_online, pressure, temperature |
| `srp_telemetry` | High-frequency surface pump data | timestamp, spm, stroke, vfd_hz, current, voltage, power, torque, surface_load_reference, position_reference |
| `dynamometer_cards` | Surface & downhole pump cards | card_id, timestamp, angle_array, time_array, position_array, load_array, sampling_metadata |
| `failures` | Equipment failure logs | event_time, component, failure_mode, unsetting, workover, downtime, action |
| `constraints` | Physical & operational safety limits | parameter, lower_limit, upper_limit, unit, source, approval_date, well_applicability |

*All internal operations use SI units, bounded by `constraints`.*
