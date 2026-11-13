# Dynalene HC grade thermohydraulic screening model

## Purpose and evidence status

This report presents a **model-based screening exercise**, not a physical test. It compares five exact Dynalene HC grades using manufacturer-reported properties at 20°C. HC-10/20/30/40 properties are from the 2025 Dynalene HC Engineering Guide; HC-50 properties are from the 2020 technical data sheet. The source revisions are not harmonised, and manufacturer-reported values are not independent measurements.

## Assumed test article and operating constraints

- Straight circular pipe, internal diameter: 10 mm.
- Pipe length: 10 m.
- Absolute roughness: 1.5 μm (illustrative smooth-pipe assumption).
- Fluid property evaluation temperature: 20°C.
- Pump wire-to-fluid efficiency: 65% (fixed illustrative assumption).
- Equal-mass-flow case: 0.400 kg/s for every grade.
- Equal-volumetric-flow case: 0.000350 m³/s for every grade.
- Equal-pump-electric-power case: 50 W input for every grade.

## Correlations

Reynolds and Prandtl numbers are evaluated using the manufacturer-reported density, dynamic viscosity, specific heat and conductivity. Darcy friction factor is estimated with the Churchill all-regime smooth/rough-pipe expression. The internal convection coefficient is estimated using the Gnielinski turbulent pipe correlation. All cases must fall within the selected nominal correlation envelope (Re 3,000–5,000,000; Pr 0.5–2,000). The model uses the Darcy friction factor in the Gnielinski expression.

Pressure drop is calculated using Darcy–Weisbach. Hydraulic pump power is pressure drop multiplied by volumetric flow; electrical input is hydraulic power divided by the assumed pump efficiency. Heat-capacity rate is mass flow multiplied by specific heat.

## Results

| Grade | Scenario | Mass flow (kg/s) | Re | ΔP (kPa) | Pump input (W) | Nu | Internal h (W/m²K) | Capacity rate (W/K) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| HC-10 | equal mass flow | 0.400 | 28294 | 263.4 | 136.2 | 245.0 | 12836 | 1328 |
| HC-10 | equal volumetric flow | 0.416 | 29461 | 283.0 | 152.4 | 254.0 | 13308 | 1383 |
| HC-10 | equal pump electric power | 0.278 | 19695 | 138.9 | 50.0 | 177.0 | 9273 | 924 |
| HC-20 | equal mass flow | 0.400 | 24252 | 262.5 | 130.6 | 223.6 | 11696 | 1285 |
| HC-20 | equal volumetric flow | 0.433 | 26250 | 302.0 | 162.6 | 240.1 | 12558 | 1391 |
| HC-20 | equal pump electric power | 0.282 | 17127 | 142.3 | 50.0 | 163.3 | 8541 | 907 |
| HC-30 | equal mass flow | 0.400 | 20372 | 265.4 | 128.1 | 201.3 | 10450 | 1231 |
| HC-30 | equal volumetric flow | 0.446 | 22727 | 321.8 | 173.3 | 222.3 | 11536 | 1373 |
| HC-30 | equal pump electric power | 0.284 | 14476 | 145.8 | 50.0 | 147.4 | 7650 | 875 |
| HC-40 | equal mass flow | 0.400 | 18863 | 262.2 | 122.7 | 191.1 | 9727 | 1172 |
| HC-40 | equal volumetric flow | 0.460 | 21704 | 335.6 | 180.7 | 217.0 | 11047 | 1349 |
| HC-40 | equal pump electric power | 0.289 | 13611 | 148.1 | 50.0 | 141.7 | 7212 | 846 |
| HC-50 | equal mass flow | 0.400 | 15915 | 268.3 | 123.2 | 169.5 | 8561 | 1080 |
| HC-50 | equal volumetric flow | 0.469 | 18661 | 354.6 | 190.9 | 196.1 | 9903 | 1267 |
| HC-50 | equal pump electric power | 0.288 | 11457 | 151.2 | 50.0 | 125.0 | 6311 | 778 |

## Interpretation

The model ranks HC-10 highest in internal-side heat-transfer coefficient under all three illustrative constraints, followed by the other grades in grade order. At equal pump electrical input, the model solves a distinct mass flow for each grade; HC-10 carries the highest mass flow and heat-capacity rate in this scenario. This is a conditional model result, not a general product ranking.

The predicted pressure drops are substantial for this small-bore, 10 m pipe at the selected flow rates. These values illustrate the strong dependence of hydraulic cost on geometry and flow. They should not be treated as recommended operating points.

## Limitations

1. The pipe, roughness, pump efficiency and operating constraints are assumed, not measured.
2. Manufacturer tables do not state uncertainty or a common test method; HC-50 comes from an earlier source revision than the other grades.
3. The model treats properties as constant at 20°C throughout the pipe; it does not integrate property variation along a thermal trajectory.
4. The model does not include fittings, valves, elevation, heat exchanger, external-side resistance, wall resistance, fouling, pump curves, NPSH/cavitation, or control-system dynamics.
5. The Gnielinski correlation estimates internal forced convection only. It does not predict total exchanger duty without geometry, wall boundary conditions and the external thermal circuit.
6. Equal pump electrical power assumes a constant 65% efficiency, whereas actual pump efficiency varies with operating point.
7. The screening does not establish chemical, electrical, corrosion, compatibility, safety, environmental or lifecycle equivalence.

## Reproducibility

Run `python scripts/model_hc_grade_screening.py` from the repository root. It reads the exact 20°C observations from `data/coolant_observations.csv` and writes `reports/hc_grade_hydraulic_screening.csv`. The script uses only the Python standard library.

## Required next step

Validate the model with a calibrated loop using the same test section and independently measured fluid properties. Conduct separate equal-mass-flow, equal-volumetric-flow and equal-pump-electric-power runs, with repeat measurements and uncertainty propagation. Do not use this screening model as a design guarantee.
