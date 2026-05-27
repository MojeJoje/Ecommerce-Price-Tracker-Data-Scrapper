#!/usr/bin/env python
"""Simple test to verify fixes work."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from amazon_scraper import AmazonScraper
    
    print("Testing Amazon Scraper...")
    scraper = AmazonScraper(use_proxies=False)
    
    # Test with demo data
    products = scraper.search_products('laptop', max_pages=1)
    
    print("[OK] Got {} products".format(len(products)))
    if products:
        print("[OK] First product name: {}".format(products[0].get('name', 'N/A')))
        print("[OK] All fixes working!")
        sys.exit(0)
    else:
        print("[FAIL] No products returned")
        sys.exit(1)
        
except Exception as e:
    print("[ERROR] {}".format(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)
