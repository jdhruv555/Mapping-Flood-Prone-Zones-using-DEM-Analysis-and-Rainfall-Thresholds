#!/usr/bin/env python3
"""
Setup script for Flood Inundation Mapping Project
Project P6: Mapping Flood-Prone Zones using DEM Analysis and Rainfall Thresholds

This script helps set up the project environment and install dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating project directories...")
    
    directories = [
        "data/dem",
        "data/rainfall", 
        "data/validation",
        "outputs/maps",
        "outputs/statistics",
        "outputs/reports"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")

def check_qgis():
    """Check if QGIS is available"""
    print("🔍 Checking QGIS availability...")
    
    # Try to import QGIS Python API
    try:
        import qgis.core
        print("✅ QGIS Python API available")
        return True
    except ImportError:
        print("⚠️  QGIS Python API not found")
        print("   Note: QGIS scripts will need to be run within QGIS environment")
        return False

def check_gee():
    """Check if Google Earth Engine is available"""
    print("🔍 Checking Google Earth Engine availability...")
    
    try:
        import ee
        print("✅ Google Earth Engine API available")
        return True
    except ImportError:
        print("⚠️  Google Earth Engine API not found")
        print("   Install with: pip install earthengine-api")
        print("   Then authenticate with: earthengine authenticate")
        return False

def create_sample_data():
    """Create sample data for testing"""
    print("📊 Creating sample data...")
    
    try:
        from scripts.data_processing import DataProcessor
        
        project_path = Path(__file__).parent
        processor = DataProcessor(project_path)
        results = processor.run_processing()
        
        if results['success']:
            print("✅ Sample data created successfully")
            print(f"   DEM: {results['dem_file']}")
            print(f"   Rainfall: {results['rainfall_file']}")
        else:
            print("❌ Failed to create sample data")
            
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("🎉 Project setup completed!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Download actual DEM data from USGS Earth Explorer")
    print("2. Download rainfall data from CHIRPS")
    print("3. Download Sentinel-1 data from Copernicus Open Access Hub")
    print("4. Run QGIS workflow: python scripts/qgis_workflow.py")
    print("5. Run GEE workflow: Execute scripts/gee_workflow.js in GEE")
    print("6. Generate final report using the template in outputs/reports/")
    
    print("\n🔗 Useful Links:")
    print("- USGS Earth Explorer: https://earthexplorer.usgs.gov/")
    print("- CHIRPS Rainfall: https://www.chc.ucsb.edu/data/chirps")
    print("- Copernicus Open Access Hub: https://scihub.copernicus.eu/")
    print("- QGIS Documentation: https://docs.qgis.org/")
    print("- Google Earth Engine: https://earthengine.google.com/")
    
    print("\n📚 Documentation:")
    print("- README.md: Project overview and setup instructions")
    print("- documentation/methodology.md: Detailed methodology")
    print("- documentation/results.md: Expected results and analysis")
    print("- outputs/reports/Project_Report_Template.md: Report template")

def main():
    """Main setup function"""
    print("🚀 Setting up Flood Inundation Mapping Project")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("⚠️  Some packages may not have installed correctly")
    
    # Check software availability
    qgis_available = check_qgis()
    gee_available = check_gee()
    
    # Create sample data
    create_sample_data()
    
    # Print next steps
    print_next_steps()
    
    print("\n✅ Setup completed successfully!")

if __name__ == "__main__":
    main()
