"""Configuration settings for the e-commerce price tracker."""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Amazon Configuration
AMAZON_BASE_URL = "https://www.amazon.com"
AMAZON_SEARCH_URL = "https://www.amazon.com/s"

# Scraping Configuration
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 2

# Proxy Configuration
USE_ROTATING_PROXIES = True
PROXY_LIST = [
    # Add your proxies here
    # Format: "http://ip:port" or "http://user:pass@ip:port"
]

# Browser Configuration
SELENIUM_HEADLESS = True
SELENIUM_WINDOW_SIZE = "1920,1080"

# Output Configuration
OUTPUT_FORMAT = "excel"  # "excel" or "csv"
PRICE_HISTORY_FILE = OUTPUT_DIR / "price_history.xlsx"
CSV_EXPORT_FILE = OUTPUT_DIR / "products.csv"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = BASE_DIR / "logs.txt"

# Default search queries
DEFAULT_SEARCH_QUERIES = [
    "laptop",
    "smartphone",
    "wireless headphones",
]
