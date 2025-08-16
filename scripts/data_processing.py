#!/usr/bin/env python3
"""
Data Processing Script for Flood Inundation Mapping
Project P6: Mapping Flood-Prone Zones using DEM Analysis and Rainfall Thresholds
"""

import os
import sys
import numpy as np
import pandas as pd
import rasterio
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataProcessor:
    """Data processing class for flood inundation mapping"""
    
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.data_path = self.project_path / "data"
        
        # Create data directories
        self.data_path.mkdir(exist_ok=True)
        (self.data_path / "dem").mkdir(exist_ok=True)
        (self.data_path / "rainfall").mkdir(exist_ok=True)
        (self.data_path / "validation").mkdir(exist_ok=True)
        
        # Study area parameters (Kosi Basin, Bihar)
        self.study_area = {
            'name': 'Kosi Basin, Bihar, India',
            'bbox': [85.5, 25.5, 88.5, 27.5],
            'crs': 'EPSG:4326'
        }
        
        logger.info(f"Initialized Data Processor for {self.study_area['name']}")
    
    def create_sample_dem(self, output_filename="srtm_kosi_basin.tif"):
        """Create sample DEM data for demonstration"""
        logger.info("Creating sample DEM data...")
        
        output_path = self.data_path / "dem" / output_filename
        
        # Create sample elevation data
        height, width = 1000, 1000
        elevation_data = np.random.uniform(0, 1000, (height, width))
        
        # Create geotransform for Kosi Basin
        transform = rasterio.transform.from_bounds(
            self.study_area['bbox'][0], self.study_area['bbox'][1],
            self.study_area['bbox'][2], self.study_area['bbox'][3],
            width, height
        )
        
        # Save as GeoTIFF
        with rasterio.open(
            output_path,
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=elevation_data.dtype,
            crs=self.study_area['crs'],
            transform=transform
        ) as dst:
            dst.write(elevation_data, 1)
        
        logger.info(f"Sample DEM created: {output_path}")
        return str(output_path)
    
    def create_sample_rainfall(self, output_filename="chirps_kosi_basin.tif"):
        """Create sample rainfall data for demonstration"""
        logger.info("Creating sample rainfall data...")
        
        output_path = self.data_path / "rainfall" / output_filename
        
        # Create sample rainfall data
        height, width = 1000, 1000
        rainfall_data = np.random.exponential(50, (height, width))
        
        # Create geotransform for Kosi Basin
        transform = rasterio.transform.from_bounds(
            self.study_area['bbox'][0], self.study_area['bbox'][1],
            self.study_area['bbox'][2], self.study_area['bbox'][3],
            width, height
        )
        
        # Save as GeoTIFF
        with rasterio.open(
            output_path,
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=rainfall_data.dtype,
            crs=self.study_area['crs'],
            transform=transform
        ) as dst:
            dst.write(rainfall_data, 1)
        
        logger.info(f"Sample rainfall data created: {output_path}")
        return str(output_path)
    
    def run_processing(self):
        """Run complete data processing workflow"""
        logger.info("Starting data processing workflow...")
        
        results = {
            'dem_file': self.create_sample_dem(),
            'rainfall_file': self.create_sample_rainfall(),
            'success': True
        }
        
        logger.info("Data processing completed successfully!")
        return results

def main():
    project_path = Path(__file__).parent.parent
    processor = DataProcessor(project_path)
    
    results = processor.run_processing()
    
    print("\n=== Data Processing Results ===")
    print(f"Study Area: {processor.study_area['name']}")
    print(f"DEM File: {results['dem_file']}")
    print(f"Rainfall File: {results['rainfall_file']}")
    print(f"Success: {results['success']}")

if __name__ == "__main__":
    main()
