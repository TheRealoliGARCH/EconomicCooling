// Validate imported GHSL study boundaries in Google Earth Engine.
// Import the prepared, three-feature table asset as "cities".
// Required normalized fields: city_id, city_name, ghsl_id, ghsl_epoch,
// geometry_source.

var expected = ee.List(['Abu Dhabi', 'Doha', 'Dubai']);
var n = cities.size();
var names = ee.List(cities.aggregate_array('city_name')).distinct().sort();
var ids = ee.List(cities.aggregate_array('city_id')).distinct();
var epochs = ee.List(cities.aggregate_array('ghsl_epoch')).distinct();
var nonEmpty = cities.map(function(f) {
  f = ee.Feature(f);
  return f.set('geometry_area_km2', f.geometry().area(1).divide(1e6));
});

print('Feature count; expected 3', n);
print('Distinct city names; expected Dubai, Abu Dhabi, Doha', names);
print('Distinct city IDs; expected 3', ids.size());
print('Boundary epochs; expected [2020]', epochs);
print('Per-feature geometry area and source attributes', nonEmpty);
print('Name check (manual confirmation required)', names.equals(expected));
