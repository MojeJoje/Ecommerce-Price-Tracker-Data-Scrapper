#!/usr/bin/env python
"""Test script to verify all imports work correctly."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from config import *
    print("✓ config imported successfully")
    
    from proxy_manager import ProxyManager
    print("✓ proxy_manager imported successfully")
    
    from amazon_scraper import AmazonScraper
    print("✓ amazon_scraper imported successfully")
    
    from data_processor import DataProcessor
    print("✓ data_processor imported successfully")
    
    from scraper import EcommerceScraper
    print("✓ scraper imported successfully")
    
    from main import main
    print("✓ main imported successfully")
    
    print("\n✓✓✓ All imports successful! Project is ready to run. ✓✓✓")
    
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
