"""Amazon product scraper using BeautifulSoup and Selenium."""

import logging
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

from config import (
    AMAZON_SEARCH_URL,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    SELENIUM_HEADLESS,
)
from proxy_manager import ProxyManager

logger = logging.getLogger(__name__)


class AmazonScraper:
    """Scrapes product data from Amazon."""

    def __init__(self, use_proxies: bool = False, proxy_list: List[str] = None):
        """
        Initialize Amazon scraper.

        Args:
            use_proxies: Whether to use rotating proxies
            proxy_list: List of proxy URLs
        """
        self.ua = UserAgent()
        self.proxy_manager = ProxyManager(proxy_list) if use_proxies else None
        self.session = requests.Session()
        self.max_retries = MAX_RETRIES

    def get_headers(self) -> Dict[str, str]:
        """Get headers with random user agent."""
        return {
            "User-Agent": self.ua.random,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Connection": "keep-alive",
        }

    def search_products(
        self, search_query: str, max_pages: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Search for products on Amazon.

        Args:
            search_query: Search query string
            max_pages: Maximum number of pages to scrape

        Returns:
            List of product dictionaries
        """
        products = []
        for page in range(1, max_pages + 1):
            logger.info(f"Scraping page {page} for query: {search_query}")
            page_products = self._scrape_search_page(search_query, page)
            products.extend(page_products)
        return products

    def _scrape_search_page(
        self, search_query: str, page: int
    ) -> List[Dict[str, Any]]:
        """Scrape a single search results page."""
        params = {
            "k": search_query,
            "page": page,
        }

        for attempt in range(self.max_retries):
            try:
                headers = self.get_headers()
                proxies = (
                    self.proxy_manager.get_proxies_dict()
                    if self.proxy_manager
                    else None
                )

                response = self.session.get(
                    AMAZON_SEARCH_URL,
                    params=params,
                    headers=headers,
                    proxies=proxies,
                    timeout=REQUEST_TIMEOUT,
                )
                response.raise_for_status()

                return self._parse_search_results(response.content)

            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    import time

                    time.sleep(RETRY_DELAY)
                else:
                    logger.error(f"Failed to scrape page {page} after {self.max_retries} attempts")
                    return []

    def _parse_search_results(self, content: bytes) -> List[Dict[str, Any]]:
        """Parse HTML content and extract product information."""
        soup = BeautifulSoup(content, "lxml")
        products = []

        # Amazon product listing selectors
        product_elements = soup.select("div[data-component-type='s-search-result']")

        for element in product_elements:
            try:
                product = self._extract_product_info(element)
                if product:
                    products.append(product)
            except Exception as e:
                logger.debug(f"Error parsing product element: {e}")
                continue

        return products

    def _extract_product_info(self, element) -> Dict[str, Any]:
        """Extract product information from a product element."""
        try:
            # Product name
            name_elem = element.select_one("span[data-component-type='s-title'] span")
            name = name_elem.text.strip() if name_elem else "N/A"

            # Product price
            price_elem = element.select_one("span.a-price-whole")
            price = price_elem.text.strip() if price_elem else "N/A"

            # Product rating
            rating_elem = element.select_one("span[aria-label*='out of 5']")
            rating = rating_elem.get("aria-label", "N/A") if rating_elem else "N/A"

            # Product URL
            url_elem = element.select_one("h2 a")
            product_url = (
                "https://www.amazon.com" + url_elem["href"]
                if url_elem and "href" in url_elem.attrs
                else "N/A"
            )

            # Stock status (simplified)
            stock_elem = element.select_one("span.a-icon-prime")
            in_stock = "Prime" in element.text

            return {
                "name": name,
                "price": price,
                "rating": rating,
                "url": product_url,
                "in_stock": in_stock,
                "source": "Amazon",
            }
        except Exception as e:
            logger.debug(f"Error extracting product info: {e}")
            return None

    def close(self) -> None:
        """Close the session."""
        self.session.close()
