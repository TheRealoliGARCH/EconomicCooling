# Local Python Satellite Pipeline (Ubuntu/Linux)

This is the primary execution route for the EconomicCooling satellite panel.
Google Earth Engine is not required. The workflow is local, reproducible, and
designed to preserve source resolution and provenance.

## 1. Environment

Install Miniforge (or another Conda-compatible distribution), then from the
repository root run:

```bash
conda env create -f environment.yml
conda activate economiccooling
python -c "import geopandas, rasterio, xarray, h5py; print('environment OK')"
```

The environment is defined through conda-forge because GDAL/PROJ-backed
geospatial packages are more reliably resolved together than through a
mixed system-Python/pip installation.

## 2. GHSL boundary discovery

The fixed-boundary main specification uses GHSL WUP MTUC R2025A epoch 2020
for Dubai, Abu Dhabi, and Doha. The archive is the official V1_1 vector release.

```bash
python scripts/inspect_ghsl_archive.py --download
```

The script downloads, integrity-checks, extracts, and inventories the archive.
It writes `reports/ghsl_layer_inventory.json` containing layer names, fields,
CRS, feature counts, and sample attributes.

**Do not assume field names or city-name spellings.** Inspect the inventory and
complete `data/city_boundary_selection.csv` with the exact layer, field names,
and values. Verify the country and epoch as well as the city label.

Then run:

```bash
python scripts/prepare_city_boundaries.py
```

The script uses exact reviewed matches; it does not use fuzzy matching. If
multiple features match one city, it retains them separately and flags the
need for a documented aggregation decision. Review the output geometries
before using them for raster extraction.

## 3. Data acquisition and processing sequence

1. **GHSL:** acquire and review the fixed 2020 urban-centre geometry.
2. **MODIS MOD11A2.061:** acquire 8-day, 1 km Terra daytime/nighttime LST
   tiles covering the study polygons; apply product QA before annual summaries.
3. **ERA5-Land:** retrieve 2 m temperature and dewpoint for the study region.
   Its native grid is approximately 0.1 degrees (~9–11 km), not 1 km.
   Reprojection to a finer grid is only a spatial alignment operation and
   must not be represented as higher-resolution meteorological information.
4. **VIIRS VNP46A4 Collection 2:** acquire annual Black Marble radiance for
   2012 onward using NASA LAADS DAAC authenticated access; preserve quality
   flags and valid-pixel coverage.
5. **Population:** choose and document a consistent population product and
   record whether each year is observed, interpolated, or projected.
6. **Panel:** aggregate to the agreed city-grid-year schema, with explicit
   missingness and quality coverage.

## 4. Authentication

Never commit access tokens or API keys to Git. Keep them in environment
variables or the relevant user-level configuration file.

- NASA LAADS scripted downloads require an authorized download token.
  The LAADS API V2 is the current API; the Classic API was retired in 2026.
- ERA5-Land CDS API requests require a Copernicus Climate Data Store account,
  an API key in the user-level CDS configuration, and acceptance of the
  dataset terms of use.

## 5. Research integrity

- MODIS LST is land-surface skin temperature, not indoor temperature or
  near-surface air temperature.
- ERA5-Land is substantially coarser than the target 1 km grid.
- VIIRS radiance is a proxy for activity, not GDP, output, or productivity.
- Population-weighted outdoor exposure is a spatial proxy, not measured
  individual or indoor exposure.
- A cooling intervention is not coded as treatment merely because a district
  cooling plant exists. Require commissioning dates and actual service
  coverage/connection evidence.
- Keep raw data immutable; store checksums, source identifiers, product
  collection/version, retrieval date, QA rules, and processing parameters.
- Do not estimate a monetary Cooling Dividend without defensible economic
  outcomes and a counterfactual design.

## Official data documentation

- GHSL WUP MTUC R2025A: https://human-settlement.emergency.copernicus.eu/ghs_wup_mtuc.php
- MODIS MOD11A2.061: https://doi.org/10.5067/MODIS/MOD11A2.061
- ERA5-Land: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land
- NASA LAADS API V2: https://ladsweb.modaps.eosdis.nasa.gov/tools-and-services/api-v2/quick-start-guide/
- NASA VNP46A4 archive: https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VNP46A4/

## Current status

This repository contains workflow code and specifications, not downloaded
satellite observations. No GHSL geometry has yet been selected or validated,
and no satellite panel has been generated.
