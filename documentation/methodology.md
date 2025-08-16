# Methodology: Flood Inundation Mapping using DEM and Rainfall

## Project Overview
**Project Code**: P6  
**Title**: Mapping Flood-Prone Zones using DEM Analysis and Rainfall Thresholds  
**Study Area**: Kosi Basin, Bihar, India  
**Objective**: To identify flood-prone and inundation areas by integrating topographic data (Digital Elevation Models) and historical rainfall patterns using GIS and remote sensing tools.

## Study Area Description

### Kosi Basin, Bihar, India
- **Geographic Coordinates**: 25.5°N to 27.5°N, 85.5°E to 88.5°E
- **Area**: Approximately 74,500 sq km
- **Characteristics**: 
  - River basin with frequent flooding events
  - Known for river course changes
  - High vulnerability to monsoon floods
  - Agricultural land with dense population

## Data Sources and Preprocessing

### 1. Digital Elevation Model (DEM)
**Source**: SRTM 30m Global Digital Elevation Model  
**URL**: https://earthexplorer.usgs.gov/  
**Processing Steps**:
- Download SRTM tiles covering Kosi Basin
- Mosaic multiple tiles into single DEM
- Clip to study area boundary
- Fill sinks to remove topographic depressions
- Validate elevation values and spatial resolution

### 2. Rainfall Data
**Source**: CHIRPS (Climate Hazards Group InfraRed Precipitation with Station data)  
**URL**: https://www.chc.ucsb.edu/data/chirps  
**Processing Steps**:
- Download daily rainfall data for monsoon period (July 2022)
- Calculate total rainfall accumulation
- Identify heavy rainfall events (>200mm/day)
- Spatial interpolation for consistent coverage

### 3. Satellite Imagery for Validation
**Source**: Sentinel-1 SAR  
**URL**: https://scihub.copernicus.eu/  
**Processing Steps**:
- Download Sentinel-1 GRD data for flood period
- Apply speckle filtering
- Extract VV and VH polarization bands
- Classify water bodies using backscatter thresholds

## Methodology

### QGIS Workflow

#### Step 1: DEM Processing
1. **Load DEM Data**
   - Import SRTM DEM into QGIS
   - Set coordinate reference system (WGS84)
   - Verify spatial extent and resolution

2. **Generate Hillshade**
   - Use QGIS Hillshade tool
   - Parameters: Azimuth 315°, Altitude 45°
   - Output: Visual representation of terrain

3. **Calculate Slope and Aspect**
   - Use QGIS Slope tool
   - Output: Slope raster in degrees
   - Use QGIS Aspect tool
   - Output: Aspect raster in degrees

#### Step 2: Hydrological Analysis
4. **Fill Sinks**
   - Use QGIS Fill Sinks tool
   - Remove topographic depressions
   - Prepare DEM for flow analysis

5. **Calculate Flow Direction**
   - Use QGIS Flow Direction tool
   - D8 algorithm for flow direction
   - Output: Flow direction raster

6. **Calculate Flow Accumulation**
   - Use QGIS Flow Accumulation tool
   - Based on flow direction
   - Output: Flow accumulation raster

7. **Delineate Watershed**
   - Use QGIS Basin tool
   - Define outlet points
   - Output: Watershed boundary vector

#### Step 3: Flood Risk Assessment
8. **Define Flood Thresholds**
   - Elevation threshold: <50m above sea level
   - Slope threshold: <5 degrees
   - Flow accumulation threshold: >1000 cells
   - Rainfall threshold: >200mm/day

9. **Classify Flood-Prone Zones**
   - Combine multiple criteria using raster calculator
   - Low elevation + Low slope + High flow accumulation
   - Overlay with rainfall data
   - Output: Flood risk classification raster

10. **Vectorize Results**
    - Convert raster to vector polygons
    - Calculate area statistics
    - Output: Flood-prone area boundaries

### Google Earth Engine Workflow

#### Step 1: Data Loading
```javascript
// Load DEM
var dem = ee.Image('USGS/SRTMGL1_003').clip(studyArea);

// Load rainfall data
var rainfall = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
  .filterDate('2022-07-01', '2022-07-31')
  .filterBounds(studyArea)
  .sum();
```

#### Step 2: Topographic Analysis
```javascript
// Calculate slope
var slope = ee.Terrain.slope(dem);

// Classify low elevation areas
var lowElevation = dem.lt(50);

// Classify low slope areas
var lowSlope = slope.lt(5);
```

#### Step 3: Rainfall Analysis
```javascript
// Classify heavy rainfall areas
var heavyRainfall = rainfall.gt(200);
```

#### Step 4: Flood Risk Classification
```javascript
// Combine criteria for flood risk
var floodRisk = lowElevation.and(lowSlope).and(heavyRainfall);
```

#### Step 5: Sentinel-1 Validation
```javascript
// Load Sentinel-1 data
var sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterDate('2022-07-01', '2022-07-31')
  .filterBounds(studyArea)
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .mosaic();

// Extract VV band and classify water
var vv = sentinel1.select('VV');
var waterMask = vv.lt(-12);
```

#### Step 6: Final Classification
```javascript
// Combine flood risk prediction with actual water detection
var finalClassification = ee.Image(0)
  .where(floodRisk.and(waterMask), 3)  // Confirmed flood
  .where(floodRisk, 2)  // High risk
  .where(waterMask, 1);  // Water detected
```

## Classification Scheme

### Flood Risk Categories
1. **No Risk (0)**: Areas above flood thresholds
2. **Water Detected (1)**: Areas with water detected by Sentinel-1
3. **High Risk (2)**: Areas meeting flood risk criteria
4. **Confirmed Flood (3)**: Areas with both risk prediction and water detection

### Threshold Parameters
- **Elevation**: <50m above sea level
- **Slope**: <5 degrees
- **Flow Accumulation**: >1000 cells
- **Rainfall**: >200mm/day
- **Sentinel-1 VV**: <-12 dB

## Validation Methods

### 1. Historical Flood Records
- Compare results with historical flood extent maps
- Validate against known flood events in Kosi Basin
- Assess accuracy of flood-prone area identification

### 2. Sentinel-1 SAR Validation
- Use Sentinel-1 water extent as ground truth
- Calculate accuracy metrics (Overall Accuracy, Kappa)
- Validate flood prediction against actual water detection

### 3. Field Validation
- Ground truth data collection (if available)
- Comparison with local flood records
- Stakeholder consultation and validation

## Output Products

### 1. Raster Maps
- DEM and hillshade
- Slope and aspect maps
- Flow direction and accumulation
- Flood risk classification
- Rainfall distribution

### 2. Vector Maps
- Watershed boundaries
- Flood-prone area polygons
- Infrastructure overlay

### 3. Statistics
- Area calculations for each risk category
- Percentage of study area affected
- Population and infrastructure at risk

### 4. Final Map Layout
- Comprehensive flood inundation map
- Legend and scale bar
- Metadata and methodology description

## Quality Assurance

### Data Quality Checks
- DEM resolution and accuracy verification
- Rainfall data temporal consistency
- Sentinel-1 data quality assessment
- Coordinate system validation

### Processing Validation
- Cross-validation between QGIS and GEE results
- Comparison with existing flood maps
- Sensitivity analysis of threshold parameters

### Output Validation
- Visual inspection of results
- Statistical analysis of classifications
- Expert review and validation

## Limitations and Considerations

### Data Limitations
- DEM resolution affects accuracy of flood modeling
- Rainfall data temporal resolution impacts flood prediction
- Sentinel-1 availability during flood events

### Methodological Limitations
- Simplified hydrological modeling approach
- Static threshold-based classification
- Limited consideration of infrastructure and land use

### Future Improvements
- Integration of land use/land cover data
- Dynamic threshold adjustment based on historical data
- Machine learning approaches for classification
- Real-time flood monitoring system

## References

1. USGS Earth Explorer - SRTM Data: https://earthexplorer.usgs.gov/
2. CHIRPS Rainfall Data: https://www.chc.ucsb.edu/data/chirps
3. Copernicus Open Access Hub: https://scihub.copernicus.eu/
4. QGIS Documentation: https://docs.qgis.org/
5. Google Earth Engine Documentation: https://developers.google.com/earth-engine

---

**Note**: This methodology provides a comprehensive framework for flood inundation mapping. The actual implementation may require adjustments based on data availability, study area characteristics, and specific project requirements.
