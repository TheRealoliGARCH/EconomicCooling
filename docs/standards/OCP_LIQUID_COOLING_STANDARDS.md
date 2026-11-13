# OCP liquid-cooling standards register

**Research snapshot:** 12 November 2026  
**Purpose:** Record public OCP documents that can inform the Coolants research protocol. This file summarises requirements; it does not reproduce the standards or certify any product.

## 1. PG25 single-phase propylene-glycol coolant

**Document:** *Base Specification for Single-Phase Propylene Glycol-Based Cold Plate Coolants (PG 25), Version 1.0.0*, dated 14 July 2026.  
**Official document:** https://www.opencompute.org/documents/ocp-base-specification-pg25-v1-0-0-final-pdf/  
**Scope:** Supplier requirements for inhibited PG-based fluids used in single-phase direct-to-chip cold-plate systems.

Key requirements recorded for research screening:

- Propylene glycol purity: at least 99.5% for the PG feedstock.
- Finished-fluid composition: 25–28% PG by mass (approximately 24.5–27.5% by volume, formulation-dependent).
- Ready-to-use finished fluid; no end-user dilution required.
- Finished-fluid pH: 7.5–10.5.
- Silicate-based additives prohibited; specified restrictions/recommendations also apply to siloxane antifoam and amines.
- Defined water-quality and finished-fluid impurity limits, including conductivity and metal/anion limits.
- Final filtration: 50 μm or finer, with 25 μm or finer preferred.
- Corrosion protection evaluated using modified ASTM D8040 with copper, brass and stainless-steel coupons; specified exposure is 88°C for two weeks with aeration and corrosive salts. The document gives metal-specific maximum coupon weight losses.
- Thermal-stability screening uses a modified ASTM D7437 procedure with hardness contamination at 90°C for two weeks; precipitate below 0.25 mL is the stated screening criterion.
- Shipment documentation includes a certificate of analysis; the TDS must report viscosity, heat capacity, density and thermal conductivity across the expected operating-temperature range, including the lowest anticipated temperature.

**Critical interpretation:** The specification explicitly says it does not mandate a common formulation and that compliance does not establish interchangeability or functional equivalence between suppliers. The Coolants project must therefore treat PG25 compliance as a qualification attribute, not as proof that two fluids are equivalent.

## 2. Single-phase water-based cold-plate coolant

**Document:** *Base Specification for Single Phase Water-Based Cold Plate Coolants*, Version 1.3, effective 6 August 2026.  
**Official document:** https://www.opencompute.org/documents/base-specification-for-single-phase-water-based-cold-plate-coolant-v1-3-final-pdf/  
**Scope:** Water-based fluids for single-phase cold-plate cooling in the OCP ecosystem.

Research-relevant requirements include:

- Water-based formulation compatible with wetted materials in the technology-cooling-system loop.
- Corrosion inhibitor for copper; additional protection is required where aluminium is present, including attention to galvanic corrosion.
- pH range 8.0–10.5.
- Purified water with low conductivity, dissolved solids, hardness and turbidity.
- Specified fresh-fluid screening limits include total suspended solids below 5 ppm, total dissolved solids below 2,000 ppm, conductivity below 2,000 μS/cm, total hardness below 30 ppm as CaCO3, turbidity below 5 NTU, and total viable bacteria below 1 CFU/mL.
- The document also specifies corrosion-performance targets and certificate-of-analysis expectations.

**Comparability warning:** This water-based specification and the PG25 specification are different qualification regimes. A fluid passing one regime must not be presumed comparable to a fluid passing the other.

## 3. Single-phase direct-to-chip cold-plate test specification

**Document:** *OCP Cold Plate Test Specification*, Version 1.0.0, dated 11 August 2026.  
**Official document:** https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf  
**Scope:** Vendor-neutral test methods and conditions for design/prototype qualification of single-phase direct-to-chip cold plates.

The test suite spans:

- Leakage and pressure integrity.
- Thermal resistance and hydraulic pressure-drop/flow performance.
- Mechanical robustness.
- Environmental and reliability exposure.
- Material/fluid compatibility and cleanliness.

For thermal-resistance testing, the specification describes measuring cold-plate sink temperature, inlet-fluid temperature, applied power, flow rate and pressure drop, and calculating thermal resistance as R = (Ts - Tl)/P. It calls for repeated measurements at multiple flow rates to produce a performance curve. This supports our decision to treat coolant properties and component-level system performance as separate but linked datasets.

The test specification defines measurement methods and conditions; it does not itself prescribe all product-specific design targets. Its scope is design and prototype qualification, not routine factory acceptance testing.

## 4. Implications for the Coolants research design

1. **Separate product identity from state observations.** A product catalogue row is not a temperature-specific property measurement.
2. **Capture exact concentration basis.** PG25 mass fraction and volume fraction are not interchangeable. Store both only when the source reports them or a documented conversion is possible.
3. **Require final-formulation property data.** For PG25, the OCP specification requires TDS properties to be measured on the formulated finished fluid, not merely inferred from neat base chemicals.
4. **Separate fluid qualification from cold-plate qualification.** A coolant's corrosion/chemistry qualification does not establish cold-plate hydraulic or thermal performance.
5. **Build equivalence conditionally.** Candidate fluids must be compared under matched geometry, operating temperature, pressure, flow constraint, material set and test protocol.
6. **Record compliance evidence explicitly.** Use fields for specification/version, test method, result, laboratory, date, sample/batch and evidence status. Never infer compliance from a product-family label such as PG25.
7. **Preserve uncertainty and provenance.** A stated typical value, specification limit, certificate-of-analysis result and independent laboratory measurement are different evidence classes.

## 5. Source limitations

This register is a research summary of the named public documents as accessed on 12 November 2026. Before a formal compliance claim, retrieve the complete current specification, verify amendments/errata, and inspect the underlying test reports or certificates. The Coolants repository is an independent research project and is not an OCP certification body.
