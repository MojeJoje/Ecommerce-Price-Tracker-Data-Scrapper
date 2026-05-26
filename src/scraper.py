"""Main scraper orchestrator."""

import logging
from typing import List, Dict, Any
from amazon_scraper import AmazonScraper
from data_processor import DataProcessor
from config import DEFAULT_SEARCH_QUERIES, OUTPUT_DIR

logger = logging.getLogger(__name__)


class EcommerceScraper:
    """Main scraper for e-commerce price tracking."""

    def __init__(self, use_proxies: bool = False, proxy_list: List[str] = None):
        """
        Initialize the e-commerce scraper.

        Args:
            use_proxies: Whether to use rotating proxies
            proxy_list: List of proxy URLs
        """
        self.amazon_scraper = AmazonScraper(use_proxies, proxy_list)
        self.data_processor = DataProcessor(OUTPUT_DIR)
        self.products = []

    def scrape_amazon(
        self, search_queries: List[str] = None, max_pages: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Scrape products from Amazon.

        Args:
            search_queries: List of search queries
            max_pages: Maximum pages per search query

        Returns:
            List of scraped products
        """
        queries = search_queries or DEFAULT_SEARCH_QUERIES
        products = []

        for query in queries:
            logger.info(f"Starting Amazon scrape for: {query}")
            query_products = self.amazon_scraper.search_products(query, max_pages)
            products.extend(query_products)

        self.products.extend(products)
        logger.info(f"Total products scraped from Amazon: {len(products)}")
        return products

    def export_products(self, format: str = "excel", filename: str = None) -> str:
        """
        Export products to file.

        Args:
            format: Export format ('excel' or 'csv')
            filename: Custom output filename

        Returns:
            Path to output file
        """
        if format.lower() == "excel":
            default_filename = filename or "products.xlsx"
            output_path = self.data_processor.save_to_excel(
                self.products, default_filename
            )
        elif format.lower() == "csv":
            default_filename = filename or "products.csv"
            output_path = self.data_processor.save_to_csv(
                self.products, default_filename
            )
        else:
            logger.error(f"Unsupported format: {format}")
            return None

        return str(output_path)

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about scraped products."""
        if not self.products:
            return {
                "total_products": 0,
                "sources": {},
                "in_stock_count": 0,
                "average_rating": "N/A",
            }

        sources = {}
        for product in self.products:
            source = product.get("source", "Unknown")
            sources[source] = sources.get(source, 0) + 1

        in_stock = sum(1 for p in self.products if p.get("in_stock", False))

        return {
            "total_products": len(self.products),
            "sources": sources,
            "in_stock_count": in_stock,
            "out_of_stock_count": len(self.products) - in_stock,
        }

    def close(self) -> None:
        """Clean up resources."""
        self.amazon_scraper.close()
