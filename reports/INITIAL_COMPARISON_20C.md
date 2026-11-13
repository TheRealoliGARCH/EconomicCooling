# Initial cross-chemistry comparison at 20°C

**Research snapshot:** 12 November 2026  
**Purpose:** Illustrate the first comparison enabled by the source-audited property dataset. This is a screening calculation, not a controlled performance test.

## Method

Compare the 40 vol% DOWFROST HD observation series with the manufacturer-published Dynalene HC-50 series at 20°C.

- Dynalene HC-50 values are directly reported at 20°C in the manufacturer's SI property table.
- DOWFROST HD has reported points at 10°C and 40°C; its 20°C values are obtained by straight-line interpolation between those two points.
- No extrapolation is used.
- The four properties are compared separately. This table does not imply equal heat-transfer coefficient, equal pressure drop, or system-level equivalence.

## Property comparison

| Property | DOWFROST HD, 40 vol% | Dynalene HC-50 | HC-50 relative to DOWFROST |
|---|---:|---:|---:|
| Specific heat, kJ/(kg K) | 3.601 (interpolated) | 2.701 (reported) | -25.0% |
| Thermal conductivity, W/(m K) | 0.4007 (interpolated) | 0.505 (reported) | +26.0% |
| Density, kg/m³ | 1050.18 (interpolated) | 1340 (reported) | +27.6% |
| Dynamic viscosity, mPa s | 5.5578 (interpolated) | 3.20 (reported) | -42.4% |

## Interpretation

The first comparison already demonstrates why a scalar ranking of coolants is inadequate. At 20°C, the HC-50 table reports higher thermal conductivity and lower dynamic viscosity than the interpolated DOWFROST HD 40 vol% values, but also lower specific heat and higher density.

These differences do not determine a winner. Specific heat influences sensible heat capacity per unit mass; conductivity influences conductive transport; density and viscosity jointly influence Reynolds number, mass flow at a given volumetric flow, pressure loss and pump power. Their system effects depend on the operating constraint and heat-exchanger geometry.

## Important limitations

1. The products are not concentration-matched: DOWFROST is identified at 40% propylene glycol by volume; the HC-50 TDS identifies a named potassium-formate grade but does not disclose its potassium-formate mass fraction in the cited table.
2. The DOWFROST value at 20°C is interpolated, not directly reported.
3. The HC-50 and DOWFROST tables do not provide a common measurement protocol, uncertainty budget, or explicit pressure basis in the extracted tables.
4. Manufacturer-reported values are not independent laboratory measurements.
5. This is a property comparison only. It does not establish equal heat-transfer coefficients, pressure-drop curves, corrosion performance, electrical compatibility, or lifecycle cost.

## Next experiment

A controlled comparison should use a common test loop, matched inlet temperature and heat load, documented material coupons, calibrated flow and differential-pressure sensors, and a defined control variable (equal mass flow, equal volumetric flow, or equal pump power). Results should be reported under all three flow constraints where practicable, since the ranking can change with the constraint.
