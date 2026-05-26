"""Main entry point for the e-commerce price tracker."""

import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from scraper import EcommerceScraper
from config import LOG_LEVEL, LOG_FILE

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def main():
    """Run the main scraper."""
    logger.info("Starting E-commerce Price Tracker")

    try:
        # Initialize scraper
        scraper = EcommerceScraper(use_proxies=False)  # Set to True to use proxies

        # Scrape Amazon
        logger.info("Scraping Amazon...")
        search_queries = ["laptop", "smartphone"]
        products = scraper.scrape_amazon(search_queries, max_pages=1)

        if products:
            logger.info(f"Successfully scraped {len(products)} products")

            # Export to Excel
            logger.info("Exporting products to Excel...")
            excel_path = scraper.export_products(format="excel")
            logger.info(f"Excel file saved to: {excel_path}")

            # Export to CSV
            logger.info("Exporting products to CSV...")
            csv_path = scraper.export_products(format="csv", filename="products.csv")
            logger.info(f"CSV file saved to: {csv_path}")

            # Print statistics
            stats = scraper.get_statistics()
            logger.info(f"Statistics: {stats}")

        else:
            logger.warning("No products were scraped")

    except Exception as e:
        logger.error(f"Error during scraping: {e}", exc_info=True)
        sys.exit(1)

    finally:
        scraper.close()
        logger.info("E-commerce Price Tracker completed")


if __name__ == "__main__":
    main()
