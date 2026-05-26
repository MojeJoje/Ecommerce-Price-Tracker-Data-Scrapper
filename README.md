# E-commerce Price Tracker

A Python-based web scraper that tracks product prices across multiple e-commerce platforms (starting with Amazon). Delivers clean, structured data in Excel and CSV formats with price change logging capabilities.

## Features

- **Multi-platform scraping**: Amazon (expandable to other retailers)
- **Product data extraction**: Name, price, rating, stock status, URL
- **Rotating proxy support**: For large-scale scraping
- **Multiple export formats**: Excel (XLSX) and CSV
- **Price history tracking**: Monitor price changes over time
- **Error handling & retry logic**: Robust scraping with auto-retry
- **Logging**: Comprehensive logging for debugging and monitoring

## Project Structure

```
├── src/
│   ├── config.py              # Configuration settings
│   ├── scraper.py             # Main scraper orchestrator
│   ├── amazon_scraper.py      # Amazon-specific scraper
│   ├── data_processor.py      # Data processing and export
│   ├── proxy_manager.py       # Proxy rotation management
│   └── main.py                # Entry point
├── data/                      # Input data directory
├── output/                    # Output files (Excel/CSV)
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or navigate to the project directory**:
   ```bash
   cd "E-commerce price tracker Data Scrapping"
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit `src/config.py` to customize:

- **Search queries**: Modify `DEFAULT_SEARCH_QUERIES`
- **Proxy settings**: Add proxies in `PROXY_LIST` and set `USE_ROTATING_PROXIES = True`
- **Output format**: Change `OUTPUT_FORMAT` between "excel" and "csv"
- **Request settings**: Adjust `REQUEST_TIMEOUT`, `MAX_RETRIES`, `RETRY_DELAY`

## Usage

### Basic Usage

Run the scraper with default settings:

```bash
python src/main.py
```

### Advanced Usage

Use the scraper programmatically:

```python
from src.scraper import EcommerceScraper

# Create scraper instance
scraper = EcommerceScraper(use_proxies=False)

# Scrape Amazon with custom queries
products = scraper.scrape_amazon(
    search_queries=["laptop", "smartphone", "headphones"],
    max_pages=2
)

# Export results
excel_file = scraper.export_products(format="excel")
csv_file = scraper.export_products(format="csv")

# Get statistics
stats = scraper.get_statistics()
print(stats)

# Clean up
scraper.close()
```

## Output

### Excel File (products.xlsx)
- Structured product data
- Formatted columns for easy viewing
- Suitable for business analysis
- Price history sheet for tracking changes

### CSV File (products.csv)
- Plain text format
- Import into databases or other tools
- Compatible with data analysis tools

## Features in Detail

### 1. **Amazon Scraper**
- Extracts: Product name, price, rating, URL, stock status
- Uses BeautifulSoup for parsing HTML
- Implements anti-detection measures (random user agents)
- Handles timeouts and retries automatically

### 2. **Data Processor**
- Converts raw data to structured format
- Removes duplicates
- Filters by stock status, price range
- Exports in multiple formats
- Adds metadata (scrape timestamp)

### 3. **Proxy Manager**
- Rotates proxies to avoid IP blocking
- Supports sequential and random proxy selection
- Easy proxy list management

### 4. **Error Handling**
- Automatic retry on network failures
- Detailed logging of all operations
- Graceful degradation

## Portfolio Tips

### Before/After Comparison
To showcase your skills:

1. **Raw HTML Output**: Screenshot or save raw HTML responses
   - Shows complex, unstructured data
   - Highlights the challenge of extraction

2. **Clean Table Output**: Export and visualize the processed data
   - Shows clear, organized results
   - Demonstrates data transformation

3. **Documentation**: Include this README and code comments
   - Shows professionalism and maintainability

## Requirements

### Core Dependencies
- `beautifulsoup4`: HTML parsing
- `requests`: HTTP requests
- `pandas`: Data manipulation
- `openpyxl`: Excel file creation
- `selenium`: JavaScript rendering (optional)
- `scrapy`: Alternative scraping framework (optional)

See `requirements.txt` for full list and versions.

## Customization

### Adding New Retailers

1. Create a new scraper class (e.g., `ebay_scraper.py`)
2. Implement the same interface as `AmazonScraper`
3. Add to the main `EcommerceScraper` class
4. Update configuration as needed

### Example:
```python
from ebay_scraper import EbayScraper

scraper = EcommerceScraper()
ebay_scraper = EbayScraper()
products = ebay_scraper.search_products("laptop")
```

## Troubleshooting

### Common Issues

**Issue**: "ModuleNotFoundError: No module named 'bs4'"
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: Connection timeouts
- **Solution**: Increase `REQUEST_TIMEOUT` in `config.py`
- **Solution**: Check internet connection
- **Solution**: Try enabling proxies

**Issue**: No products found
- **Solution**: Check that search query is valid
- **Solution**: Verify HTML selectors haven't changed on website
- **Solution**: Check logs for detailed error messages

**Issue**: IP blocked by website
- **Solution**: Enable rotating proxies in `config.py`
- **Solution**: Increase `RETRY_DELAY` to add delays between requests

## Logging

Logs are saved to `logs.txt` and printed to console. Check them for:
- Scraping progress
- Errors and warnings
- Performance metrics
- Debugging information

Adjust `LOG_LEVEL` in `config.py` to control verbosity.

## Performance Tips

1. **Reduce pages**: Start with `max_pages=1` to test
2. **Use proxies**: For large-scale scraping (100+ products)
3. **Parallel requests**: Consider using `asyncio` for concurrent scraping
4. **Cache responses**: Implement caching to avoid re-scraping same products

## Legal & Ethical Considerations

- **Review Terms of Service**: Check if scraping is allowed
- **Rate limiting**: Don't overwhelm servers with requests
- **Respect robots.txt**: Follow website's scraping guidelines
- **Use responsibly**: Only scrape the data you need
- **Attribution**: Credit the data source appropriately

## Future Enhancements

- [ ] Multi-threading/async scraping
- [ ] Database storage (SQLite, PostgreSQL)
- [ ] Scheduled scraping (cron jobs)
- [ ] Price change alerts
- [ ] Web dashboard for visualization
- [ ] Additional retailers (eBay, Walmart, Best Buy, etc.)
- [ ] Competitor price comparison
- [ ] API for programmatic access

## Support

For issues or questions:
1. Check `logs.txt` for error details
2. Review configuration in `src/config.py`
3. Verify all dependencies are installed
4. Check HTML selectors against current website structure

## License

This project is provided as-is for educational and portfolio purposes.

## Author

Created as an e-commerce price tracking solution.

---

**Happy scraping! 🚀**
