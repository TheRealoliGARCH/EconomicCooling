# GHSL urban-boundary import guide

## Official source

Download the **GHS-WUP-MTUC R2025A vector** package from the European Commission Joint Research Centre:

- Product description: https://human-settlement.emergency.copernicus.eu/ghs_wup_mtuc_r2025a.php
- Download page: https://human-settlement.emergency.copernicus.eu/GHSWUPDownload.php?ds=WUPMTUC
- Current vector archive resolved by the download page: `GHS_WUP_MTUC_GLOBE_R2025A_V1_1_vector.zip`

The product contains multitemporal urban-centre polygons and population-weighted centroid points. The official page's descriptive metadata may still show V1_0 naming; record the archive's actual V1_1 version. Cite the JRC dataset as Schiavina et al. (2025), GHS-WUP-MTUC R2025A, DOI 10.2905/1ea967e5-bedc-4cf3-a0b0-3851742ee7e2.

## Main boundary rule

For the primary 2000–2025 panel, select the **2020 boundary** for each of Dubai, Abu Dhabi and Doha and hold it fixed across all years. This avoids changing the composition of the spatial sample as urban areas expand.

For robustness, repeat using the time-varying boundary epochs 2000, 2005, 2010, 2015, 2020 and 2025. The 2025 boundary is a modelled projection and must not be treated as a purely observed boundary.

## Prepare the boundary file

1. Download and unzip the V1_1 vector archive.
2. Open the multitemporal urban-centre polygon shapefile in QGIS.
3. Inspect the attribute table and identify the fields corresponding to:
   - stable urban-centre identifier (expected: `ID_UC_G0`);
   - boundary identifier (expected: `ID_MTUC`);
   - urban-centre name (expected: `UCname`);
   - country name (expected: `UNLocName`);
   - boundary epoch (expected: `Year`).
4. Filter to `Year = 2020`.
5. Identify the correct urban-centre entities for Dubai, Abu Dhabi and Doha using both the name and country fields. Do not assume that an urban centre has exactly the same extent as a municipality or metropolitan planning region. If more than one GHSL urban centre corresponds to a study area, document the selection or aggregation decision before proceeding.
6. Export only the selected three features to a new GeoPackage or Shapefile. Reproject to WGS84 (EPSG:4326) for Earth Engine ingestion. Keep the original GHSL IDs and epoch fields.
7. Add these normalized properties to each feature:
   - `city_id`: stable project key, e.g. `DXB_UAE`, `AUH_UAE`, `DOH_QAT`;
   - `city_name`: exactly `Dubai`, `Abu Dhabi`, or `Doha`;
   - `ghsl_id`: original stable GHSL urban-centre ID;
   - `ghsl_epoch`: 2020;
   - `geometry_source`: `GHS-WUP-MTUC R2025A V1_1`.
8. Upload the small selected vector file as a table asset in the Google Earth Engine Code Editor. Import the asset into the script and name the imported variable `cities`.

Do not replace or discard original GHSL attributes. Do not simplify the geometry unless the export fails; if simplification is necessary, retain the unsimplified source and record the tolerance.

## Validation before extraction

Run `scripts/validate_city_boundary_asset.js` after importing the asset as `cities`. Confirm:
- exactly three features are selected for the pilot;
- one feature per intended city;
- all three have `ghsl_epoch = 2020`;
- country and GHSL IDs match the downloaded source table;
- geometries are non-empty and plausibly located;
- city names and IDs are unique.

If the GHSL entity match is ambiguous, stop and resolve the city definition rather than selecting the nearest polygon by intuition.

## Earth Engine export

Once validated, run `scripts/export_satellite_panel_gee.js`. The script exports MODIS and ERA5-Land thermal indicators. It does not download VIIRS Black Marble or population grids; those remain separate acquisition and merge tasks.

## Important caveats

- GHSL urban-centre boundaries are harmonized statistical geographies, not municipal legal boundaries.
- GHSL MTUC boundaries are multitemporal and at 1 km source resolution.
- A fixed 2020 boundary provides spatial comparability but excludes parts of the urban footprint that developed outside that boundary in earlier/later periods.
- The time-varying-boundary robustness analysis changes the spatial composition and should not be interpreted as a pure within-place panel.
- GHS-WUP-POP values after 2020 are projections. Store an observed/projected flag.
