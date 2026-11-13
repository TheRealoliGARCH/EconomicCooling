# Economic Cooling

**Research programme:** *Economic Cooling — from coolant thermophysics and cooling architecture to economic value, observation, reconstruction, and information.*

This repository develops a connected research programme around the physical, engineering and economic dimensions of cooling. It begins with commercial coolant properties and thermohydraulic performance, then extends to cooling-system architecture, economic value, empirical measurement, and the broader theory of observing and reconstructing complex systems.

The repository is therefore organised around **Economic Cooling**, not solely around a general theory of coolant fluids. Coolant thermophysics is its engineering foundation; the wider programme investigates how cooling capacity is designed, deployed, valued and studied empirically.

## Research objectives

1. Characterise commercial coolants using source-audited thermophysical data.
2. Model heat transfer, pressure loss, pumping power, phase behaviour and chemical stability.
3. Define condition-specific thermohydraulic equivalence under explicit operating constraints and uncertainty.
4. Study cooling-system architecture and the interaction of its physical components.
5. Analyse the economic role of cooling infrastructure, including costs, benefits and the proposed cooling dividend.
6. Develop empirical methods for studying cooling and its economic consequences.
7. Establish observation and reconstruction methods for complex physical and economic systems.
8. Study sequential information acquisition, reconstruction compatibility and the ethical use of interviews.

## Treatise series

The repository contains the following connected works:

1. [A General Theory of Coolants](1.%20A%20General%20Theory%20of%20Coolants.pdf)
2. [The General Theory of Thermohydraulic Equivalence](2.%20The%20General%20Theory%20of%20Thermohydraulic%20Equivalence.pdf)
3. [The General Theory of Cooling Architecture](3.%20The%20General%20Theory%20of%20Cooling%20Architecture.pdf)
4. [The General Theory of Economic Cooling](4.%20The%20General%20Theory%20of%20Economic%20Cooling.pdf)
5. [The General Theory of the Cooling Dividend Function](5.%20The%20General%20Theory%20of%20the%20Cooling%20Dividend%20Function.pdf)
6. [The Empirical Economics of Cooling](6.%20The%20Empirical%20Economics%20of%20Cooling.pdf)
7. [The General Theory of Transcendental Observation and Economic Reconstruction](7.%20The%20General%20Theory%20of%20Transcendental%20Observation%20and%20Economic%20Reconstruction.pdf)
8. [The General Theory of Observation Geometry and Economic Reconstruction](8.%20The%20General%20Theory%20of%20Observation%20Geometry%20and%20Economic%20Reconstruction.pdf)
9. [The Economics of Sequential Observation](9.%20The%20Economics%20of%20Sequential%20Observation.pdf)
10. [The General Theory of the Interview](10.%20The%20General%20Theory%20of%20the%20Interview.pdf)

The sequence moves from the physical properties of coolants to thermohydraulic equivalence, cooling architecture and economic analysis. It then develops the observation, reconstruction and information-acquisition foundations needed to study complex systems. The treatises articulate a research programme; their inclusion does not imply that every theoretical proposition has been independently validated or that every proposed capability has been implemented in software.

## Engineering and coolant-data programme

The repository maintains a reproducible empirical and computational programme for comparing commercial coolants.

### Repository map

- `data/products.csv` — product-level catalogue; one row per identified commercial formulation.
- `data/coolant_observations.csv` — long-form property table; one row per product/state observation.
- `data/source_register.csv` — source provenance and evidence classification.
- `data/pending/dynalene_pg_2025_70F.csv` — provisional PG-series property extraction kept separate because concentration basis and exact additive subfamily remain unconfirmed.
- `docs/DATA_DICTIONARY.md` — field definitions, units and controlled vocabularies.
- `docs/METHODOLOGY.md` — modelling, validation and equivalence protocol.
- `docs/EXPERIMENT_PROTOCOL.md` — controlled test-loop protocol and uncertainty/reporting requirements.
- `docs/PENDING_PG_DATA.md` — PG-series provenance gap and promotion criteria.
- `docs/standards/OCP_LIQUID_COOLING_STANDARDS.md` — OCP PG25, water-based coolant and cold-plate test references.
- `scripts/validate_dataset.py` — standard-library checks for products, observations and provenance.
- `scripts/compare_coolants.py` — no-extrapolation, temperature-specific interpolation for an initial property comparison.
- `scripts/model_hc_grade_screening.py` — Churchill/Gnielinski pipe-flow model for the five Dynalene HC grades.
- `scripts/build_hc_performance_surface.py` — exact-common-temperature, multi-flow HC performance surface generator.
- `reports/hc_performance_surface.csv` — 330 model-estimated grade-temperature-flow operating points.
- `reports/DYNALENE_HC_PERFORMANCE_SURFACE.md` — surface domain, model, results and limitations.
- `reports/hc_grade_hydraulic_screening.csv` — model-estimated outputs under three explicit flow/power constraints.
- `reports/DYNALENE_HC_THERMOHYDRAULIC_SCREENING.md` — assumptions, equations, results and limitations.
- `reports/INITIAL_COMPARISON_20C.md` — first DOWFROST HD / Dynalene HC-50 screening comparison.
- `reports/comparison_at_20C.csv` — machine-readable DOWFROST HD / HC-50 property comparison at 20°C.
- `reports/DYNALENE_HC_GRADE_SCREENING_20C.md` — descriptive comparison of all five Dynalene HC grades at 20°C.
- `reports/dynalene_hc_grade_screening_20c.csv` — machine-readable grade-level screening values.

## Evidence and modelling policy

Manufacturer technical data sheets are preferred for product properties. Product directories are discovery aids, not measurement sources. A product listing, safety data sheet, typical value, guaranteed limit, certificate-of-analysis result and independent laboratory measurement are different evidence types and must never be conflated.

No missing value is silently imputed. No property is extrapolated beyond its documented range without explicit labelling. Concentration basis (mass, volume or mole fraction) must be recorded when known.

Model outputs are estimates conditional on their inputs, assumptions, correlations and domains of validity. They are not experimental measurements. Comparisons must identify the operating conditions and constraints under which they hold.

### Initial empirical seed

The master observation table contains 137 rows across DOWFROST HD, Therminol 75 and five Dynalene HC grade series. The product catalogue contains 10 records and the source register contains 13 sources. HC property observations span grade-specific ranges from -50°C to 218°C; the master table also contains separate vapour-pressure-only observations where the guide provides a value without a matching property row. Not every observation contains every property. The original seed includes six DOWFROST HD observations for 40% propylene glycol by volume and two Therminol 75 observations.

The catalogue contains the two initial products, three Dynalene family-level leads (PG, low-conductivity LC-PG and potassium-formate HC), and exact HC-10/20/30/40/50 grade records. Family-level leads must not be treated as exact formulations or concentration-specific observations. These records are a pipeline seed, not a representative or complete market sample. HC-10/20/30/40 values are from the 2025 engineering guide; HC-50 values remain sourced from the 2020 TDS. Manufacturer tables do not provide measurement uncertainty or detailed test-method metadata in the cited sources; these are not independent laboratory data. Source documents and limitations are recorded in `data/source_register.csv`.

### Expanded Dynalene HC cohort

The 2025 Dynalene HC Engineering Guide has been added as a distinct source. Grade-specific SI property tables for HC-10, HC-20, HC-30 and HC-40, together with the multi-grade vapour-pressure table, are incorporated as a separate grade-specific data cohort. HC-50 remains separately sourced from its 2020 TDS pending source harmonisation. Grade suffixes are identifiers, not disclosed mass or volume fractions; concentration basis remains unknown. Vapour pressure is converted from psia to kPa absolute using 1 psi = 6.894757293 kPa. The guide does not state measurement uncertainty, test method or property-table pressure basis.

The consolidated observation table includes 102 additional 2025-guide rows for HC-10/20/30/40, including grade-specific vapour-pressure points. A reproducible model screens all five grades under equal mass flow, equal volumetric flow and equal pump electrical power. A second model maps 22 exact common temperatures and three mass-flow setpoints (330 grade-temperature-flow rows), flagging points outside the selected Gnielinski correlation envelope. The Dynalene PG guide's property tables have been transcribed provisionally at 70°F into a separate pending file; concentration basis and exact additive subfamily are not explicit, so those observations are not merged into the master dataset.

## OCP liquid-cooling standards

The repository records the 2026 OCP PG25 specification, the single-phase water-based coolant specification (V1.3), and the single-phase direct-to-chip cold-plate test specification (V1.0.0). These documents establish useful qualification and test frameworks. OCP explicitly cautions that PG25 specification compliance does not establish interchangeability or functional equivalence between suppliers.

## Observation, reconstruction and sequential acquisition

The observation-related treatises extend the project beyond coolant measurement. They investigate how observation systems can be constructed, how different observation geometries can be evaluated, and how incomplete observations can be used to reconstruct an underlying phenomenon.

The conceptual architecture distinguishes a foundational mathematical construction from specialised observation geometries such as equidistant, adaptive and hybrid designs. These are not necessarily competing foundations: specialised designs are evaluated as components built upon a common observation framework.

Reconstruction compatibility is central. Differences between observations may reflect different domains, temporal references, resolution, measurement quality or model assumptions; they may also reflect genuine unresolved ambiguity. Disagreement should be investigated against evidence and constraints rather than settled arbitrarily.

Sequential observation frames additional information acquisition as a decision under costs, delays and residual risk. The value of further observation must be assessed against its expected contribution to reconstruction and decision quality.

## Interviews and information ethics

The interview treatise extends information acquisition to information held by individuals and institutions. An interview is not direct observation of the underlying phenomenon; it is an interaction through which information, evidence, interpretations and incentives may be elicited.

The framework considers interviews as information-theoretic games involving cooperation and competition. It addresses interview-group selection, top-down and bottom-up inquiry, psychology, behavioural economics, leadership, reconstruction compatibility and the lifecycle of an interview.

Information acquisition is constrained by informed participation, confidentiality, purpose limitation, investigative honesty and legitimate non-disclosure. The governing distinction is:

**Information acquisition is not unrestricted information extraction.**

The broader research principle is:

**A better observatory must not become a worse society.**

These are research principles and proposed extensions. They should not be interpreted as evidence that an automated interview system, distributed observatory or global information network has already been implemented in this repository.

## Satellite-derived economic cooling panel

A pilot satellite panel for Dubai, Abu Dhabi and Doha is being developed as a separate empirical workstream. The primary execution route is local Python on Ubuntu/Linux; Google Earth Engine is not required.

- `docs/SATELLITE_PANEL_PROTOCOL.md` — measurement, spatial, temporal and identification protocol.
- `docs/UBUNTU_PYTHON_PIPELINE.md` — local installation and execution instructions.
- `environment.yml` — conda-forge environment specification.
- `scripts/inspect_ghsl_archive.py` — GHSL archive download, extraction and layer inventory.
- `data/city_boundary_selection.csv` — explicit, reviewed city-boundary matching worksheet.
- `scripts/prepare_city_boundaries.py` — create fixed-2020 study geometries after the mapping is reviewed.
- `data/satellite_panel_schema.csv` — empty panel schema, not observations.

The workflow has not yet downloaded satellite observations or validated city boundaries. It distinguishes MODIS land-surface temperature, ERA5-Land coarse-grid air temperature, VIIRS nighttime radiance and population proxies; none is treated as a direct measure of GDP or productivity.

## Reproducibility

Run the dataset validator:

```bash
python scripts/validate_dataset.py
```

The validator uses only the Python standard library. It checks schema, identifiers, source links, units, evidence labels and basic physical plausibility; it does not certify the correctness of manufacturer data or establish standards compliance.

For the satellite-panel environment, see `environment.yml` and `docs/UBUNTU_PYTHON_PIPELINE.md`. Read individual scripts and reports alongside their stated assumptions, data coverage and limitations.

## Scope and limitations

Thermohydraulic equivalence is conditional on geometry, flow constraint, temperature, pressure, boundary conditions, material set and model validity. It does not imply chemical, electrical, materials, safety, environmental or lifecycle equivalence.

The empirical seed is not a representative market sample. Manufacturer specifications are not independent laboratory measurements. Modelled operating points do not establish field performance. The satellite panel remains a pilot workflow until observations and boundary validation are completed. The observation, reconstruction and interview treatises set out a wider research programme; their proposals should be distinguished from implemented software and independently validated results.

## Long-run objective

The long-run objective of **Economic Cooling** is to connect physical cooling, cooling infrastructure, economic performance and the theory of observation into a disciplined programme of empirical and computational research. Each stage requires explicit measurement, source provenance, reconstruction, uncertainty assessment and evaluation of costs and consequences.

The intellectual progression is from **coolants**, to **cooling systems**, to the **economics of cooling**, and then to the broader problem of **how complex systems are observed, understood and reconstructed**.
