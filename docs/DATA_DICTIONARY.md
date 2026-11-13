# Data dictionary

The repository separates the product catalogue from the state-observation table. The product catalogue contains one row per identified product or explicitly labelled product-family lead; the observation table contains one row per product at one reported thermodynamic state.

## Product catalogue: data/products.csv

| Field | Meaning |
|---|---|
| product_id | Stable identifier for an exact formulation/concentration or a clearly labelled family lead; only exact formulation IDs may be referenced by property observations |
| manufacturer | Manufacturer or responsible supplier |
| product_name | Exact commercial designation |
| product_family | Broad commercial family |
| fluid_chemistry | Broad chemistry classification; do not infer proprietary formulation details |
| phase_regime | `single_phase`, `two_phase`, or `mixed_or_unknown` |
| application | Intended application as documented or conservatively classified |
| concentration_value | Numeric concentration when explicitly reported |
| concentration_unit | Unit for concentration, e.g. percent |
| concentration_basis | `mass`, `volume`, `mole`, `unknown`, or `not_applicable` |
| ready_to_use | Ready-to-use status; `unknown` where not established |
| documented_temperature_min_C | Minimum documented operating/storage temperature where available |
| documented_temperature_max_C | Maximum documented operating temperature where available |
| product_page_url | Manufacturer product page |
| tds_url | Technical data sheet or product technical document |
| source_id | Foreign key to source_register.csv |
| evidence_status | Status of product identification and documentation |
| notes | Scope limits, verification requirements and qualification caveats |

Blank temperature limits mean that the repository has not yet verified the limits; they do not mean that the fluid has no operating limits. Product-level concentration must not be assumed from a different formulation of the same commercial family. A family-level discovery lead is not an exact blend and must not be used as the product_id for a quantitative observation.

## Observation table: data/coolant_observations.csv

The observation table is in long form: each row represents one formulation at one reported thermodynamic state.

### Identity and formulation

| Field | Meaning |
|---|---|
| observation_id | Unique observation identifier |
| product_id | Stable identifier matching data/products.csv |
| manufacturer | Manufacturer or responsible supplier |
| product_name | Exact commercial designation |
| chemical_family | Controlled broad chemistry classification |
| concentration_value | Numeric concentration, when applicable |
| concentration_unit | E.g. percent |
| concentration_basis | `mass`, `volume`, `mole`, `unknown`, or `not_applicable` |

Use `unknown` when a formulation grade is identifiable but its concentration fraction or basis is not disclosed. Do not equate 40% by mass with 40% by volume. Record premix/concentrate status and dilution water quality in product-level metadata when available.

### Thermodynamic state

| Field | Unit | Meaning |
|---|---|---|
| temperature_C | °C | Property measurement temperature |
| pressure_kPa | kPa absolute unless explicitly documented otherwise | Measurement pressure |

### Properties

| Field | Unit | Meaning |
|---|---|---|
| cp_kJ_kgK | kJ/(kg K) | Specific heat capacity |
| thermal_conductivity_W_mK | W/(m K) | Thermal conductivity |
| density_kg_m3 | kg/m³ | Density |
| dynamic_viscosity_mPa_s | mPa s | Dynamic viscosity |
| kinematic_viscosity_mm2_s | mm²/s | Kinematic viscosity |
| vapor_pressure_kPa | kPa absolute | Vapour pressure; source-unit conversions are recorded in notes |

Missing values remain empty. Do not infer zero from an empty cell. If converting kinematic to dynamic viscosity, use mu = rho * nu with density and viscosity at the same temperature and composition, documenting the conversion.

### Provenance

| Field | Meaning |
|---|---|
| measurement_method | Standard or method stated by source |
| evidence_type | Controlled evidence label |
| source_id | Foreign key to source_register.csv |
| source_page_or_table | Exact page, table, figure, or web section |
| notes | Qualification, extraction, conversion, or uncertainty notes |

Allowed evidence labels should distinguish at least:
- `independent_measurement`
- `manufacturer_guaranteed`
- `manufacturer_typical`
- `manufacturer_calculated`
- `secondary_compilation`
- `interpolated`
- `model_estimated`
- `simulation_output`

## Dynalene HC 2025 guide extraction

The 2025 Dynalene HC Engineering Guide provides separate SI property tables for HC-50, HC-40, HC-30, HC-20 and HC-10, plus a multi-grade vapour-pressure table. HC-10/20/30/40 observations are recorded in the master observation table under exact grade-specific product IDs. The grade suffix is not treated as a numerical concentration fraction because the guide does not disclose its basis. Vapour-pressure values in psia are converted to kPa absolute using 1 psi = 6.894757293 kPa. Where a grade has a vapour-pressure value at a temperature without a matching property row, a vapour-pressure-only observation is recorded with other properties blank. The guide does not state measurement uncertainty, test method or the pressure basis for its thermophysical-property tables.

## Data policy

1. Preserve original source units in source notes or an archival extraction file.
2. Record the exact document revision and access date.
3. Never mix concentrations or concentration bases.
4. Keep bulk, film, and wall temperatures distinct.
5. Keep absolute and gauge pressure distinct.
6. Record whether values are measured, typical, guaranteed, calculated, or estimated.
7. Do not compare fluids across different operating conditions without a validated normalisation model.
8. Attach uncertainty where published; otherwise mark it as unavailable rather than assuming zero. Record any unit conversion explicitly in notes (for example, HC-50 vapour pressure converted from psia to kPa).
9. Treat product identification, formulation specification, property observation, and standards compliance as separate evidence objects.
