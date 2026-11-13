# Dynalene PG 2025 guide: pending concentration-basis issue

## What is established

The 2025 Dynalene PG Engineering Guide publishes property tables for viscosity (Table 6), thermal conductivity (Table 7), specific heat (Table 8) and density (Table 9). Each table has concentration columns labelled 20%, 25%, 30%, 35%, 40%, 45%, 50%, 55% and 60%. The tables use °F and customary engineering units. The guide separately provides a conversion table that explicitly distinguishes volume percent from weight percent for freezing point, burst point, boiling point and specific gravity.

## What is not established

The headings of Tables 6-9 say only 'Dynalene propylene glycol concentration =' and list percentages. They do not identify those property-table percentages as mass percent or volume percent. The guide's statement that solutions can be mixed by either weight or volume, with conversions in Table 2, does not by itself establish the basis used in Tables 6-9.

The property tables also describe 'Dynalene propylene glycol solutions' generically. The guide identifies distinct additive formulations (PG, PG-FG, PG-XT, PG-V1, PG-A1) and Raw PG; it does not explicitly allocate the property tables to one exact inhibitor subfamily.

## Provisional extraction

`data/pending/dynalene_pg_2025_70F.csv` transcribes the nine concentration columns at 70°F from Tables 6-9. It converts:
- viscosity: cP to mPa·s (numerically identical);
- thermal conductivity: BTU/(hr·ft·°F) to W/(m·K), factor 1.730735;
- specific heat: BTU/(lb·°F) to kJ/(kg·K), factor 4.1868;
- density: lb/ft³ to kg/m³, factor 16.01846337;
- temperature: 70°F to 21.111111°C.

This file is intentionally separated from the master observation table. Its concentration basis is marked `unknown`, and the product description does not claim an exact additive subfamily. The values are manufacturer-reported typical data, not independent measurements.

## Promotion criteria

Before promotion into the master dataset:
1. Obtain written confirmation from Dynalene of the concentration basis used in Tables 6-9.
2. Confirm which product formulation or formulation family those tables describe.
3. Confirm whether the current 2025 guide supersedes prior property tables and identify any revisions.
4. Preserve the original customary-unit values alongside converted SI values.
5. Record test method, property pressure basis and uncertainty if the manufacturer can supply them.

Until those conditions are met, do not use these rows for concentration-matched PG-vs-HC performance ranking or product equivalence claims.