# Project P6: Flood Inundation Mapping using DEM and Rainfall

## Project Title
Mapping Flood-Prone Zones using DEM Analysis and Rainfall Thresholds

## Objective
To identify flood-prone and inundation areas by integrating topographic data (Digital Elevation Models) and historical rainfall patterns using GIS and remote sensing tools.

## Study Area
**Kosi Basin, Bihar, India**
- Geographic Coordinates: 25.5°N to 27.5°N, 85.5°E to 88.5°E
- Area: Approximately 74,500 sq km
- Known for frequent flooding events and river course changes

## Data Sources

### DEM (Digital Elevation Model)
- **SRTM 30m**: https://earthexplorer.usgs.gov/
- **ASTER GDEM**: https://search.earthdata.nasa.gov/

### Rainfall Data
- **CHIRPS Rainfall**: https://www.chc.ucsb.edu/data/chirps
- **IMD Gridded Rainfall**: India Meteorological Department

### Satellite Imagery for Validation
- **Sentinel-1 SAR**: https://scihub.copernicus.eu/
- **MODIS/Landsat**: For temporal flood visuals

## Tools Used
- **QGIS**: DEM analysis, watershed delineation, raster processing
- **Google Earth Engine (GEE)**: Rainfall time-series, Sentinel-1 flood mapping
- **Google Earth**: Visual validation and overlay

## Project Structure
```
geosatellite/
├── README.md
├── data/
│   ├── dem/
│   ├── rainfall/
│   └── validation/
├── scripts/
│   ├── qgis_workflow.py
│   ├── gee_workflow.js
│   └── data_processing.py
├── outputs/
│   ├── maps/
│   ├── statistics/
│   └── reports/
├── documentation/
│   ├── methodology.md
│   └── results.md
└── requirements.txt
```

## Methodology

### QGIS Workflow
1. Download and load DEM (SRTM or ASTER) into QGIS
2. Generate Hillshade & Slope/Aspect maps
3. Use "Fill Sinks" tool to remove topographic depressions
4. Run "Flow Direction" and "Flow Accumulation" tools
5. Delineate Watershed using "Basin" or "Catchment" extraction
6. Overlay rainfall zones or precipitation maps
7. Define flood threshold elevation
8. Classify DEM raster for flood-prone zones
9. Overlay historical flood maps for validation
10. Vectorize flood zones and calculate affected areas

### Google Earth Engine Workflow
1. Load study area and DEM in GEE
2. Load rainfall data (CHIRPS)
3. Classify zones with heavy rainfall
4. Combine elevation and rainfall for flood risk zones
5. Overlay Sentinel-1 SAR-derived water extent
6. Export results for QGIS processing

## Results
- Flood-prone areas extracted based on topography and rainfall
- Raster map showing vulnerable zones
- Area statistics (hectares/sq km)
- Final map layout with terrain, water bodies, and flood extent

## Setup Instructions

### Prerequisites
- QGIS 3.28 or higher
- Google Earth Engine account
- Python 3.8+ with required packages

### Installation
1. Clone this repository
2. Install Python dependencies: `pip install -r requirements.txt`
3. Set up QGIS with required plugins
4. Configure Google Earth Engine API

### Running the Project
1. Download DEM data for Kosi Basin
2. Download rainfall data (CHIRPS)
3. Run QGIS workflow: `python scripts/qgis_workflow.py`
4. Run GEE workflow: Execute `scripts/gee_workflow.js` in GEE
5. Generate final maps and statistics

## Expected Outcomes
- Identification of flood-prone zones in Kosi Basin
- Integration of topographic and rainfall data
- Validation using satellite imagery
- Comprehensive flood risk assessment

## Limitations
- Accuracy depends on DEM resolution and quality
- Rainfall data temporal resolution affects results
- Requires validation with historical flood records

## Contact
For questions or issues, please contact the project coordinator.

---
**Project Code**: P6  
**Duration**: 30 Days  
**Platform**: Online (Google Meet/Zoom + Google Classroom)  
**Course Coordinator**: Miss. Alisha Sinha
