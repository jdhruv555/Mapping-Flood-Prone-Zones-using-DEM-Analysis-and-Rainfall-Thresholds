/**
 * Google Earth Engine Workflow for Flood Inundation Mapping
 * Project P6: Mapping Flood-Prone Zones using DEM Analysis and Rainfall Thresholds
 */

// Study Area: Kosi Basin, Bihar, India
var studyArea = ee.Geometry.Rectangle([85.5, 25.5, 88.5, 27.5], 'EPSG:4326');

// Flood threshold parameters
var FLOOD_THRESHOLDS = {
  elevationMax: 50,
  rainfallThreshold: 200,
  vvThreshold: -12
};

function runFloodInundationMapping() {
  print('=== Flood Inundation Mapping Workflow ===');
  
  // Step 1: Load DEM
  var dem = ee.Image('USGS/SRTMGL1_003').clip(studyArea);
  Map.addLayer(dem, {min: 0, max: 1000, palette: ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}, 'DEM');
  
  // Step 2: Load rainfall data
  var rainfall = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
    .filterDate('2022-07-01', '2022-07-31')
    .filterBounds(studyArea)
    .sum();
  
  Map.addLayer(rainfall, {min: 0, max: 500, palette: ['white', 'blue', 'darkblue']}, 'Total Rainfall');
  
  // Step 3: Calculate topographic parameters
  var slope = ee.Terrain.slope(dem);
  var lowElevation = dem.lt(FLOOD_THRESHOLDS.elevationMax);
  var lowSlope = slope.lt(5);
  
  Map.addLayer(slope, {min: 0, max: 30, palette: ['green', 'yellow', 'red']}, 'Slope');
  Map.addLayer(lowElevation, {palette: ['white', 'blue']}, 'Low Elevation');
  
  // Step 4: Classify flood risk
  var heavyRainfall = rainfall.gt(FLOOD_THRESHOLDS.rainfallThreshold);
  var floodRisk = lowElevation.and(lowSlope).and(heavyRainfall);
  
  Map.addLayer(floodRisk, {palette: ['white', 'red']}, 'Flood Risk Zones');
  
  // Step 5: Load Sentinel-1 for validation
  var sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD')
    .filterDate('2022-07-01', '2022-07-31')
    .filterBounds(studyArea)
    .filter(ee.Filter.eq('instrumentMode', 'IW'))
    .mosaic();
  
  var vv = sentinel1.select('VV');
  var waterMask = vv.lt(FLOOD_THRESHOLDS.vvThreshold);
  
  Map.addLayer(vv, {min: -25, max: 0, palette: ['red', 'yellow', 'green', 'blue']}, 'Sentinel-1 VV');
  Map.addLayer(waterMask, {palette: ['blue']}, 'Water Extent');
  
  // Step 6: Final classification
  var finalClassification = ee.Image(0)
    .where(floodRisk.and(waterMask), 3)  // Confirmed flood
    .where(floodRisk, 2)  // High risk
    .where(waterMask, 1);  // Water detected
  
  Map.addLayer(finalClassification, {min: 0, max: 3, palette: ['white', 'blue', 'orange', 'red']}, 'Final Classification');
  
  // Set map center
  Map.centerObject(studyArea, 8);
  
  print('Workflow completed successfully!');
}

// Run the workflow
runFloodInundationMapping();
