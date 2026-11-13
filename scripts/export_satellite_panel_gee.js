// EconomicCooling pilot: MODIS + ERA5-Land annual 1 km grid panel
// Run in the Google Earth Engine Code Editor.
// IMPORT a GHSL WUP R2025A urban-centre FeatureCollection as "cities".
// Required properties: city_id, city_name. Select Dubai, Abu Dhabi, Doha
// and confirm each geometry is the intended GHSL urban-centre polygon.
// This script exports thermal indicators only; VIIRS VNP46A4 is acquired
// separately from NASA LAADS DAAC using Earthdata authentication.

var START_YEAR = 2000;
var END_YEAR = 2025;
var GRID_CRS = 'EPSG:6933';
var GRID_SCALE = 1000;

var selectedCities = cities.filter(ee.Filter.inList('city_name',
  ['Dubai', 'Abu Dhabi', 'Doha']));
var gridProjection = ee.Projection(GRID_CRS).atScale(GRID_SCALE);

// Create clipped 1 km cells and preserve city identifiers.
var gridCells = ee.FeatureCollection(selectedCities.map(function(city) {
  city = ee.Feature(city);
  var geom = city.geometry();
  var cells = geom.coveringGrid(gridProjection).filterBounds(geom);
  return cells.map(function(cell) {
    cell = ee.Feature(cell);
    var clipped = cell.geometry().intersection(geom, 1);
    var id = ee.String(city.get('city_id')).cat('_')
      .cat(ee.String(cell.get('system:index')));
    return ee.Feature(clipped).set({
      city_id: city.get('city_id'),
      city_name: city.get('city_name'),
      grid_id: id,
      cell_area_km2: clipped.area(1).divide(1e6),
      geometry_source: 'GHSL WUP R2025A GHS-WUP-MTUC'
    });
  });
}).flatten());

function maskModis(img, lstBand, qcBand, outName) {
  var qc = img.select(qcBand);
  var mandatoryGood = qc.bitwiseAnd(3).eq(0);
  var dataQualityGood = qc.rightShift(2).bitwiseAnd(3).eq(0);
  var emissivityAcceptable = qc.rightShift(4).bitwiseAnd(3).lte(1);
  var lstErrorAcceptable = qc.rightShift(6).bitwiseAnd(3).lte(1);
  var good = mandatoryGood.and(dataQualityGood)
    .and(emissivityAcceptable).and(lstErrorAcceptable);
  var celsius = img.select(lstBand).multiply(0.02).subtract(273.15)
    .rename(outName).updateMask(good);
  var valid = ee.Image.constant(1).rename(outName + '_valid')
    .updateMask(good).unmask(0);
  return celsius.addBands(valid).copyProperties(img, ['system:time_start']);
}

function modisAnnual(year) {
  var start = ee.Date.fromYMD(year, 1, 1);
  var end = start.advance(1, 'year');
  var collection = ee.ImageCollection('MODIS/061/MOD11A2')
    .filterDate(start, end);
  var day = collection.map(function(img) {
    return maskModis(img, 'LST_Day_1km', 'QC_Day', 'modis_day_lst_c');
  });
  var night = collection.map(function(img) {
    return maskModis(img, 'LST_Night_1km', 'QC_Night', 'modis_night_lst_c');
  });
  var dayMean = day.select('modis_day_lst_c').mean();
  var nightMean = night.select('modis_night_lst_c').mean();
  var dayValid = day.select('modis_day_lst_c_valid').mean()
    .rename('modis_day_valid_observation_share');
  var nightValid = night.select('modis_night_lst_c_valid').mean()
    .rename('modis_night_valid_observation_share');
  return dayMean.addBands(nightMean).addBands(dayValid).addBands(nightValid);
}

function era5Annual(year) {
  var start = ee.Date.fromYMD(year, 1, 1);
  var end = start.advance(1, 'year');
  var hourly = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY')
    .filterDate(start, end)
    .map(function(img) {
      var t = img.select('temperature_2m').subtract(273.15).rename('t2m_c');
      var d = img.select('dewpoint_temperature_2m').subtract(273.15)
        .rename('dewpoint_c');
      var es = t.expression('6.112 * exp((17.67 * T) / (T + 243.5))',
        {T: t}).rename('es_hpa');
      var e = d.expression('6.112 * exp((17.67 * T) / (T + 243.5))',
        {T: d}).rename('e_hpa');
      var rh = e.divide(es).multiply(100).clamp(0, 100).rename('rh_pct');
      var h30 = t.gt(30).rename('hours_gt30');
      var h35 = t.gt(35).rename('hours_gt35');
      return t.addBands(d).addBands(rh).addBands(h30).addBands(h35);
    });
  return hourly.select('t2m_c').mean().rename('era5_t2m_mean_c')
    .addBands(hourly.select('t2m_c').max().rename('era5_t2m_max_c'))
    .addBands(hourly.select('hours_gt30').sum().rename('era5_hours_t2m_gt30c'))
    .addBands(hourly.select('hours_gt35').sum().rename('era5_hours_t2m_gt35c'))
    .addBands(hourly.select('dewpoint_c').mean().rename('era5_dewpoint_mean_c'))
    .addBands(hourly.select('rh_pct').mean()
      .rename('era5_relative_humidity_mean_pct'));
}

var years = ee.List.sequence(START_YEAR, END_YEAR);
var annualTables = ee.FeatureCollection(years.iterate(function(y, acc) {
  var year = ee.Number(y);
  var image = modisAnnual(year).addBands(era5Annual(year))
    .set('year', year);
  var rows = image.reduceRegions({
    collection: gridCells,
    reducer: ee.Reducer.mean(),
    scale: GRID_SCALE,
    crs: GRID_CRS,
    tileScale: 4
  }).map(function(feature) {
    return feature.set({
      year: year,
      data_status: 'Earth Engine export; thermal indicators; not yet audited'
    });
  });
  return ee.FeatureCollection(acc).merge(rows);
}, ee.FeatureCollection([])));

Export.table.toDrive({
  collection: annualTables,
  description: 'EconomicCooling_Dubai_AbuDhabi_Doha_MODIS_ERA5_2000_2025',
  folder: 'EconomicCooling',
  fileNamePrefix: 'megacity_grid_thermal_2000_2025',
  fileFormat: 'CSV'
});

print('Selected cities', selectedCities);
print('Grid-cell count', gridCells.size());
print('Annual output rows (expected grid cells x 26)', annualTables.size());
