# Dynalene HC coolant performance surface

## Executive summary

This report maps model-estimated thermohydraulic performance across five exact Dynalene HC grades, 22 common manufacturer-reported temperatures, and three mass-flow setpoints. It contains 330 operating-point rows. No property interpolation or extrapolation is used: each property vector is taken from a published observation at the exact temperature shared by all five grades.

This is a model surface, not a physical test, equipment guarantee, or universal product ranking.

## Surface domain

- Grades: HC-10, HC-20, HC-30, HC-40, HC-50.
- Common exact temperatures (°C): -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200.
- Mass flow setpoints: 0.2, 0.3 and 0.4 kg/s.
- Straight-pipe internal diameter: 20 mm.
- Pipe length: 5 m.
- Absolute roughness: 1.5 μm.
- Assumed pump efficiency: 65%.
- Property source: exact manufacturer observation at each grade-temperature point.
- HC-10/20/30/40: 2025 Dynalene HC Engineering Guide.
- HC-50: 2020 Dynalene HC technical data sheet.

The common-temperature restriction is deliberate. HC-40 includes a 165°C point and lacks the 210°C/218°C entries present in some other grades; those unmatched points are excluded from cross-grade surface comparison.

## Governing model

For each exact property vector:
- velocity: v = mdot/(rho A);
- Reynolds number: Re = rho v D/mu;
- Prandtl number: Pr = mu cp/k;
- Darcy friction factor: Churchill all-regime expression;
- pressure loss: Darcy-Weisbach;
- hydraulic power: DeltaP times volumetric flow;
- estimated electrical pump input: hydraulic power divided by fixed assumed efficiency;
- heat-capacity rate: mdot cp.

The internal Nusselt number and heat-transfer coefficient are calculated using the Gnielinski turbulent pipe-flow correlation only where Re is between 3,000 and 5,000,000 and Pr is between 0.5 and 2,000. Outside that nominal envelope, Nusselt number and h are left blank and the row is explicitly flagged. Four of 330 points are outside the selected Gnielinski envelope; those points are not assigned an h value by this model.

## Illustrative 20°C slice at 0.3 kg/s

| Grade | Re | Pressure drop (kPa) | Pump input (W) | Internal h (W/m²K) | Heat-capacity rate (W/K) |
|---|---:|---:|---:|---:|---:|
| HC-10 | 10610 | 2.93 | 1.14 | 2621 | 996 |
| HC-20 | 9095 | 2.94 | 1.10 | 2365 | 964 |
| HC-30 | 7639 | 3.00 | 1.09 | 2084 | 923 |
| HC-40 | 7074 | 2.97 | 1.04 | 1926 | 879 |
| HC-50 | 5968 | 3.06 | 1.06 | 1665 | 810 |

At this one operating slice, the grade with the largest predicted internal h is not necessarily the grade with the lowest pressure loss or highest heat-capacity rate. These are separate performance dimensions; a scalar ranking requires an application-specific objective and constraints.

## Surface-level ranges

Across all 330 modeled operating points:
- Reynolds number: 2126 to 82144.
- Pressure drop: 0.99 to 5.97 kPa.
- Estimated pump electrical input: 0.26 to 2.80 W.
- Internal h is reported only for valid Gnielinski points.

## Limitations and interpretation

1. HC-50 data come from a 2020 TDS; the other four grade series come from a 2025 guide. The source revisions and measurement protocols are not harmonised.
2. Manufacturer tables do not provide uncertainty or a common test method. Property-table pressure basis is not stated.
3. Constant properties are used within each operating point. The model does not solve the coupled thermal trajectory or update properties as the fluid heats or cools along the pipe.
4. Pipe geometry and roughness are illustrative. Fittings, manifolds, valves, cold plates, heat exchangers, wall resistance, fouling, external convection and elevation are excluded.
5. Pump efficiency is fixed; actual pump curves and system curves must be coupled for design.
6. Gnielinski predicts internal forced convection under its applicability conditions; it is not a complete exchanger model.
7. No phase-stability, corrosion, material compatibility, electrical, toxicity, environmental or lifecycle conclusion follows from this analysis.

## Reproducibility

Run `python scripts/build_hc_performance_surface.py` from the repository root. It reads the master observation CSV, selects exact temperatures common to all five grades, and writes `reports/hc_performance_surface.csv`. The output records property source IDs, model status, and model-estimated evidence class.

## Research implication

The natural mathematical representation is a vector-valued performance surface:
`P_g(T, mdot; D, L, epsilon, eta_p)`
whose components include heat-transfer coefficient, pressure drop, pump input and heat-capacity rate. Thermohydraulic equivalence should be defined as a tolerance region over a specified operating domain and selected outcome vector—not as equality of one scalar property or one operating point.
