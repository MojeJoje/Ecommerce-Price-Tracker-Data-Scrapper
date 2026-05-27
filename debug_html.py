#!/usr/bin/env python
"""Debug script to inspect HTML structure and product extraction."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from amazon_scraper import AmazonScraper
from bs4 import BeautifulSoup

scraper = AmazonScraper(use_proxies=False)

# Search for a product
print("Fetching search page...")
params = {
    "k": "Laptop Table",
    "page": 1,
}

try:
    response = scraper.session.get(
        "https://www.amazon.com/s",
        params=params,
        headers=scraper.get_headers(),
        timeout=10,
    )
    
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find product containers
        products = soup.select("div[data-component-type='s-search-result']")
        print(f"Found {len(products)} products")
        
        if products:
            # Inspect first product
            first_product = products[0]
            print("\n=== FIRST PRODUCT HTML ===")
            print(first_product.prettify()[:2000])
            
            print("\n=== EXTRACTION TEST ===")
            # Test extraction
            extracted = scraper._extract_product_info(first_product)
            print(f"Extracted data: {extracted}")
            
            print("\n=== ALL PRODUCTS ===")
            for i, product in enumerate(products[:3]):
                data = scraper._extract_product_info(product)
                print(f"Product {i+1}: {data}")
    else:
        print(f"Error: Status code {response.status_code}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
