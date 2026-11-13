# Research methodology

## 1. Scope and comparison unit

The comparison unit is an exact commercial formulation at a specified concentration, temperature, and pressure. Products are grouped into application cohorts before ranking:

1. Water/glycol industrial and HVAC fluids.
2. Heavy-duty and automotive engine coolants.
3. Single-phase data-centre cold-plate fluids, including PG25.
4. Dielectric immersion fluids.
5. High-temperature heat-transfer fluids.
6. Refrigerants and phase-change media (separate models).

Do not publish a single cross-cohort leaderboard without a defensible common service definition.

## 2. Governing balances

For a flowing fluid, use the enthalpy balance as the general calorimetric relation:

`Qdot = mdot * (h_out - h_in)`.

For single-phase sensible heating with approximately constant specific heat:

`Qdot = mdot * cp * (T_out - T_in)`.

For an exchanger under applicable steady-state assumptions:

`Qdot = U * A * LMTD`.

At system level, include thermal storage, heat leakage, and auxiliary loads where material.

## 3. Hydraulic model

For pipe flow, Darcy-Weisbach gives:

`DeltaP = f_D * (L/D) * rho * v^2 / 2`.

Pump input power is:

`P_pump = DeltaP * Vdot / eta_p`.

Include fittings, valves, heat exchangers, cold plates, manifolds, filters, and connectors. The friction factor depends on Reynolds number and relative roughness. Do not assume cubic pumping-power scaling except under explicitly fixed simplifying assumptions.

## 4. Heat-transfer correlations

Use a correlation appropriate to geometry, Reynolds and Prandtl ranges, thermal development, wall boundary condition, and property-evaluation convention. Dittus-Boelter is not universal. Consider Gnielinski, Sieder-Tate, and laminar/developing-flow relations as applicable.

Properties should be evaluated consistently, e.g. bulk or film temperature as required by the correlation.

## 5. Property fitting

Candidate models include low-order polynomials for cp, k, and density over restricted measured ranges, and nonlinear temperature models for viscosity. Model selection must be based on residual diagnostics, physical plausibility, and out-of-sample performance.

Never extrapolate beyond the source range without a separate explicit model and uncertainty treatment.

## 6. Temperature-specific screening interpolation

Where a target temperature lies between two manufacturer-reported observations for the same exact formulation, simple linear interpolation may be used for preliminary screening. The interpolated value must be labelled as such, retain links to both source observations, and never be presented as a direct manufacturer measurement. No extrapolation is permitted in the screening script. More flexible property models require residual diagnostics, physical constraints, and validation against held-out temperatures or independent measurements.

## 7. Thermohydraulic equivalence

Define equivalence only after specifying:
- geometry and surface roughness;
- mass-flow or volumetric-flow constraint;
- inlet conditions and heat load;
- pressure boundary conditions;
- pump curve and efficiency;
- temperature and phase envelope;
- tolerance on thermal duty, pressure loss, and pump power.

A practical outcome vector is:

`y = [Qdot, DeltaP, P_pump, T_max, stability metrics]`.

Normalise against a reference case and use declared tolerances. A pairwise distance threshold may not be transitive; use a documented clustering or graph procedure rather than assuming mathematical equivalence classes automatically follow.

Thermohydraulic equivalence does not imply equivalence in corrosion, electrical compatibility, toxicity, flammability, environmental persistence, service life, or cost.

## 8. Economic analysis

Use total cost of ownership and lifecycle cost, including:
- fluid purchase and replacement;
- capital equipment;
- pump and auxiliary electricity;
- maintenance and monitoring;
- downtime and failure risk;
- disposal and environmental compliance.

Report NPV and levelised cost of cooling only with transparent horizon, discount rate, energy-price assumptions, and service delivered.

## 9. Statistical validation

Separate descriptive, predictive, causal, and experimental claims. Use product- or formulation-level holdouts to prevent leakage across temperatures from the same fluid. Report RMSE, MAE, residual plots, uncertainty, and external validation where possible.

Manufacturer product specifications are observational data, not randomised experiments. Correlation is not causal identification.

## 10. Evidence and source audit

Prioritise original manufacturer technical data sheets and recognised standards. Product directories are useful for discovery but are not primary measurement sources. Preserve source revision, page/table, units, concentration basis, method, and evidence type.

The 2026 OCP PG25 base specification is a relevant standardisation reference for the single-phase data-centre cohort. Retrieve and inspect the actual specification before encoding numerical acceptance criteria.

## 11. Experimental validation

A controlled test should record mass flow, inlet/outlet temperatures, pressure drop, pump electrical power, heat input, coolant composition, and instrument calibration. Compare candidate fluids under equivalent service conditions. Repeat tests and report uncertainty. Include long-duration stability, corrosion, fouling, and materials compatibility where relevant.


## Grade-level pipe-flow screening model

The HC grade screening model is a transparent single-phase pipe-flow calculation. It uses exact 20°C observations, the Churchill Darcy friction-factor expression, Darcy–Weisbach pressure loss, and the Gnielinski internal turbulent convection correlation. It reports equal-mass-flow, equal-volumetric-flow and equal-pump-electrical-power scenarios separately. Assumed pipe geometry, roughness and pump efficiency are explicit inputs. The model is not a test-loop result and does not establish whole-exchanger duty or coolant equivalence. HC-50 remains sourced from the 2020 TDS while HC-10/20/30/40 use the 2025 engineering guide.


## Temperature-dependent coolant performance surfaces

For each exact formulation and exact measured temperature, construct a vector-valued operating response using density, dynamic viscosity, specific heat and thermal conductivity. The current HC surface uses only exact temperatures common to all five grades; it performs no property interpolation or extrapolation. The surface maps temperature and mass flow conditional on fixed geometry, roughness and assumed pump efficiency. Report Re, Pr, Darcy friction factor, pressure drop, hydraulic/electrical pump power and heat-capacity rate. Calculate Gnielinski Nusselt number and internal h only within the selected correlation envelope, and flag rather than silently extrapolate outside it. This remains a pipe-flow screening model, not a full exchanger or plant model.

A useful formal representation is a vector-valued map `P_g(T, mdot; D, L, epsilon, eta_p) = (h_i, DeltaP, P_pump, mdot*cp)`. Equivalence must be conditional on a declared operating domain, system geometry, pump constraint, selected outputs and pre-specified tolerance margins. A scalar score should be introduced only after application-specific weights or constraints are justified.
