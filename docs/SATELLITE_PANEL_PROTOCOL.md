# Satellite-derived megacity panel: pilot protocol

## Purpose and scope

This protocol specifies a reproducible 1 km equal-area grid panel for Dubai, Abu Dhabi and Doha. It is a measurement layer for the Economic Cooling programme, not a completed dataset and not a causal design by itself.

The intended common satellite panel is 2012–2025 because NASA Black Marble annual VIIRS VNP46A4 begins in 2012. A separate thermal-only extension covers 2000–2025 using MODIS and ERA5-Land. Do not fill pre-2012 nighttime-light values with DMSP or another sensor without a separately documented cross-sensor harmonisation exercise.

No satellite observations have yet been downloaded or calculated by this protocol. The CSV in `data/satellite_panel_schema.csv` is an empty schema, not observations.

## Spatial frame

Use the European Commission GHSL WUP R2025A GHS-WUP-MTUC urban-centre polygons as the initial city boundary source. The official download page currently resolves to vector package V1_1; use that package and record the exact file/version. The multitemporal polygon layer contains five-year boundary epochs and stable urban-centre identifiers. Retain ID_UC_G0, ID_MTUC, UCname, UNLocName, Year and boundary vintage where present. Confirm the selected entities correspond to the intended metropolitan areas; do not assume that an administrative municipality, metropolitan region and GHSL urban centre are interchangeable. For the main 2000–2025 panel, use the 2020 boundary as a fixed spatial frame; repeat with epoch-specific boundaries only as a robustness analysis.

Download the official V1_1 vector ZIP and inspect its attribute table locally. The primary workflow is Python on Ubuntu/Linux; Google Earth Engine is not required. Use `scripts/inspect_ghsl_archive.py` to download, extract and inventory the archive, then complete `data/city_boundary_selection.csv` with exact, reviewed city/country/epoch matches. Use `scripts/prepare_city_boundaries.py` to select the 2020 features and reproject them from World Mollweide (ESRI:54009) to WGS84 (EPSG:4326). Review all selected geometries, especially cases with multiple matching features. The resulting local GeoJSON is `data/processed/cities_2020.geojson`. The normalized output has properties:
- `city_id`: stable unique identifier;
- `city_name`: one of Dubai, Abu Dhabi or Doha;
- `geometry_source`: dataset name and release;
- geometry: the selected GHSL urban-centre polygon.

The local Python grid builder will create 1 km cells in EPSG:6933 (NSIDC EASE-Grid 2.0 Global equal-area projection). Cells are clipped to the urban-centre boundary. Preserve cell area or area fraction because boundary cells are partial.

## Data products

### Thermal surface: MODIS Terra MOD11A2.061

- 8-day, 1 km land-surface-temperature composites.
- Use `LST_Day_1km` and `LST_Night_1km`, scale factor 0.02 K, then convert to Celsius.
- Apply the corresponding `QC_Day` / `QC_Night` bit masks. Retain mandatory QA=good, data quality=good, emissivity error <= 0.02 and LST error <= 2 K.
- Annual means are averages of quality-screened 8-day composites. Export valid-observation share alongside the means.
- LST is surface skin temperature under clear-sky retrieval conditions, not 2 m air temperature, indoor temperature or personal thermal exposure.

### Atmospheric exposure: ERA5-Land hourly

Use `ECMWF/ERA5_LAND/HOURLY`:
- `temperature_2m`;
- `dewpoint_temperature_2m`.

Convert Kelvin to Celsius. Calculate annual mean and maximum 2 m temperature, hours above 30 C and 35 C, mean dewpoint, and mean relative humidity derived from temperature and dewpoint using a documented saturation-vapour-pressure formula. These are grid-cell reanalysis measures; the native ERA5-Land grid is about 11 km, so resampling to 1 km does not create 1 km meteorological information. Keep that limitation visible in all analysis.

Threshold counts are descriptive and should be tested against alternative thresholds and locally relevant acclimatization/occupational standards. A universal 30 C or 35 C threshold is not a universal health or productivity threshold.

### Economic activity: NASA Black Marble VNP46A4.002

Use the same Collection 2 product version for every year 2012–2025:
- Annual moonlight/BRDF-adjusted nighttime radiance composite;
- near-nadir, snow-free composite as primary measure, with QA and observation metadata retained;
- calculate mean radiance, sum radiance, and valid/good-quality pixel share.

Black Marble data are HDF5 and require NASA Earthdata authentication through LAADS DAAC. Do not combine Collection 1 and Collection 2 annual radiance values without a documented harmonisation. Do not interpret radiance as GDP or productivity: it is a proxy for emitted nighttime light and may reflect residential lighting, public lighting, electrification, commercial activity and sensor/processing effects.

### Population

Use GHSL population grids with a documented release and epoch. Distinguish historical estimates from projections: GHS-WUP-POP R2025A is calibrated/maintained through 2020 and projected beyond that, so its 2025 value must not be described as an observed population count. For annual 2012–2025 analyses, GHSL's five-year epochs require a transparent interpolation or nearest-epoch assignment; do not silently present interpolated population as observed annual population. Prefer a consistent annual population product (e.g. a validated WorldPop series for its available years) where available. Store source year, observed/projected status and interpolation method per row.

## Grid-cell measures and aggregation

The primary spatial unit is city x 1 km cell x year. Use population weights for city-level thermal exposure:
`Theta_it = sum_g(P_git * H_git) / sum_g(P_git)`.

Retain unweighted cell means and population-weighted means separately. For nighttime lights, retain both mean radiance and summed radiance; their interpretation differs and sums depend on valid pixel area. For clipped edge cells, normalize sums by valid area or report area coverage.

A city-year population-weighted average is not equivalent to the average person's indoor exposure. It is a spatial exposure proxy.

## Cooling intervention crosswalk

Do not assign treatment to a city merely because a district-cooling plant is located there. For each project, require:
1. Verified commissioning/operational date and phase;
2. Actual service boundary or geocoded connected buildings;
3. Connected capacity or connected load by year, where possible;
4. A cell-level exposure rule (e.g. share of cell population/buildings served);
5. A defensible control area and explicit spillover rings.

Use `cooling_exposure_share` only when supported by spatial service evidence. If only distance to plant is known, store a separate distance-based proxy and label it as such; do not call it delivered cooling.

## Identification and interpretation

Nighttime radiance can rise because cooling enables activity, but also because development attracts cooling investment. Reverse causality and co-investment are central threats. A credible event study requires pre-treatment outcomes, no anticipation, comparable controls, stable boundaries, and treatment timing that reflects actual service delivery. With only three cities, city-level inference is weak; the 1 km grid increases spatial detail but does not create independent treatment assignment. Cluster/inference strategy must reflect the level at which intervention is assigned and spatial dependence.

A fall in outdoor LST is not required for district cooling to produce indoor comfort or productivity benefits. Conversely, a rise in nighttime radiance does not establish a cooling dividend. The principal hypothesis is that effective cooling provision reduces the sensitivity of economic activity to adverse thermal exposure, not necessarily that it reduces outdoor temperature.

## Reproducibility and provenance

Record:
- source collection and version;
- retrieval date;
- processing script commit;
- QA rules;
- projection and grid definition;
- urban-boundary vintage and identifiers;
- valid-observation share;
- missingness and data-quality flags;
- population source year and interpolation method;
- treatment evidence and spatial crosswalk source.

The local Python pipeline will process MODIS and ERA5-Land thermal indicators. VIIRS annual composites require a separate authenticated LAADS download/extraction workflow. The project register remains a candidate evidence inventory; its provisional project years are not accepted treatment dates.

## Official product documentation

- NASA Black Marble / VNP46 product suite and Collection 2 documentation: https://viirsland.gsfc.nasa.gov/Products/NASA/BlackMarble.html and https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP46A4
- MODIS Terra MOD11A2.061 Earth Engine data catalogue: https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD11A2
- ERA5-Land hourly Earth Engine data catalogue: https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_HOURLY
- GHSL WUP R2025A MTUC product description and download: https://human-settlement.emergency.copernicus.eu/ghs_wup_mtuc_r2025a.php and https://human-settlement.emergency.copernicus.eu/GHSWUPDownload.php?ds=WUPMTUC

The GHSL WUP R2025A MTUC dataset contains urban-centre polygons, points and multi-temporal population/built-up summary statistics. Use the published dataset citation and retain the release identifier in the project metadata.


## Boundary and temporal design correction

The official GHSL MTUC release page currently resolves to the V1_1 vector package, while the descriptive page still displays V1_0 naming. Record the actual archive name and release from the downloaded file rather than relying on the older page label. The boundary layer is multitemporal at five-year intervals and includes stable urban-centre identity fields (notably ID_UC_G0); verify field names against the downloaded attribute table before filtering.

Main specification: select each study urban centre's 2020 polygon and hold that geometry fixed for all years 2000–2025. This avoids mechanically changing the spatial sample as the city expands. Robustness specification: use epoch-specific GHSL boundaries (2000, 2005, 2010, 2015, 2020, 2025), while explicitly interpreting differences as a combination of within-boundary change and boundary expansion. The 2025 boundary and any post-2020 population estimates are modelled projections, not observed historical outcomes.

The grid is 1 km, so this is a city-grid-year panel, not a true 1 km meteorological panel: ERA5-Land retains its coarser native spatial support. Do not use spatial standard errors or degrees of freedom as though every grid cell were independently treated.


## Local Ubuntu execution route

The supported execution environment is Python 3.11 on Ubuntu/Linux using the conda-forge environment in `environment.yml`. Follow `docs/UBUNTU_PYTHON_PIPELINE.md`. Google Earth Engine is not part of the required workflow. The earlier `scripts/export_satellite_panel_gee.js` is retained as a historical/alternative implementation only; it is not the primary pipeline.

Current boundary scripts:
- `scripts/inspect_ghsl_archive.py`: download, integrity-check, extract and inventory the official GHSL V1_1 vector archive.
- `scripts/prepare_city_boundaries.py`: apply an exact, reviewed mapping from `data/city_boundary_selection.csv` and export the fixed-2020 study geometries.

No satellite observations or city boundaries have yet been downloaded, selected, or validated in this repository.
