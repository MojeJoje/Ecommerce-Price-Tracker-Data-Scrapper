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

    def get_demo_products(self, search_query: str) -> List[Dict[str, Any]]:
        """Get demo product data when scraping is blocked."""
        demo_data = {
            "laptop": [
                {
                    "name": "Lenovo ThinkPad X1 Carbon - 14 inch Laptop",
                    "price": "$899.99",
                    "rating": "4.5 out of 5 stars",
                    "url": "https://www.amazon.com/s?k=laptop",
                    "in_stock": True,
                    "source": "Amazon",
                },
                {
                    "name": "Dell XPS 13 Plus Laptop - Intel Core i7",
                    "price": "$1,099.99",
                    "rating": "4.7 out of 5 stars",
                    "url": "https://www.amazon.com/s?k=laptop",
                    "in_stock": True,
                    "source": "Amazon",
                },
                {
                    "name": "Apple MacBook Pro 14 inch M3",
                    "price": "$1,499.00",
                    "rating": "4.8 out of 5 stars",
                    "url": "https://www.amazon.com/s?k=laptop",
                    "in_stock": True,
                    "source": "Amazon",
                },
            ],
            "smartphone": [
                {
                    "name": "Samsung Galaxy S24 Ultra 512GB",
                    "price": "$1,299.99",
                    "rating": "4.6 out of 5 stars",
                    "url": "https://www.amazon.com/s?k=smartphone",
                    "in_stock": True,
                    "source": "Amazon",
                },
                {
                    "name": "Apple iPhone 15 Pro Max 256GB",
                    "price": "$1,199.99",
                    "rating": "4.7 out of 5 stars",
                    "url": "https://www.amazon.com/s?k=smartphone",
                    "in_stock": True,
                    "source": "Amazon",
                },
            ],
            "wireless headphones": [
                {
                    "name": "Sony WH-1000XM5 Wireless Headphones",
                    "price": "$399.99",
                    "rating": "4.8 out of 5 stars",
                    "url": "https://www.amazon.com/s?k=wireless+headphones",
                    "in_stock": True,
                    "source": "Amazon",
                },
                {
                    "name": "Apple AirPods Pro (2nd generation)",
                    "price": "$249.00",
                    "rating": "4.6 out of 5 stars",
                    "url": "https://www.amazon.com/s?k=wireless+headphones",
                    "in_stock": True,
                    "source": "Amazon",
                },
            ],
        }
        return demo_data.get(search_query.lower(), [])

    def get_headers(self) -> Dict[str, str]:
        """Get headers with random user agent."""
        return {
            "User-Agent": self.ua.random,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "Referer": "https://www.amazon.com/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
        }

    def search_products(
        self, search_query: str, max_pages: int = 1, use_demo: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search for products on Amazon.

        Args:
            search_query: Search query string
            max_pages: Maximum number of pages to scrape
            use_demo: Use demo data if scraping fails

        Returns:
            List of product dictionaries
        """
        products = []
        for page in range(1, max_pages + 1):
            logger.info(f"Scraping page {page} for query: {search_query}")
            page_products = self._scrape_search_page(search_query, page)
            products.extend(page_products)
        
        # Fallback to demo data if no products found and demo is enabled
        if not products and use_demo:
            logger.warning(f"No products found for '{search_query}'. Using demo data.")
            products = self.get_demo_products(search_query)
            if products:
                logger.info(f"Using {len(products)} demo products")
        
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
                import time
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
                
                # Check for 503 or other blocking status codes
                if response.status_code == 503:
                    logger.warning(f"Attempt {attempt + 1}: Amazon returned 503 (blocked)")
                    if attempt < self.max_retries - 1:
                        wait_time = RETRY_DELAY * (attempt + 2)  # Exponential backoff
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Amazon blocked access after {self.max_retries} attempts")
                        return []
                    continue
                
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
            except Exception as e:
                logger.error(f"Parsing error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error(f"Failed to parse page {page} after {self.max_retries} attempts")
                    return []

    def _parse_search_results(self, content: bytes) -> List[Dict[str, Any]]:
        """Parse HTML content and extract product information."""
        soup = BeautifulSoup(content, "html.parser")
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
        """Extract product information from a product element with robust fallbacks."""
        try:
            # Product name - try multiple selectors and image alt, and more fallbacks
            name = "N/A"
            selectors = [
                "span[data-component-type='s-title'] span",
                "h2 a span",
                "span.a-size-medium.a-color-base.a-text-normal",
                "span.a-size-base-plus.a-color-base.a-text-normal",
                "span.a-text-normal",
            ]
            for sel in selectors:
                name_elem = element.select_one(sel)
                if name_elem and name_elem.text.strip():
                    name = name_elem.text.strip()
                    break
            if name == "N/A":
                img = element.select_one("img.s-image")
                if img and img.get("alt"):
                    name = img.get("alt").strip()

            # Product price - try more selectors and patterns
            price = "N/A"
            price_whole = element.select_one("span.a-price-whole")
            price_frac = element.select_one("span.a-price-fraction")
            price_symbol = element.select_one("span.a-price-symbol")
            if price_whole:
                whole = price_whole.text.strip()
                frac = price_frac.text.strip() if price_frac else ""
                symbol = price_symbol.text.strip() if price_symbol else "$"
                if frac:
                    price = f"{symbol}{whole}.{frac}"
                else:
                    price = f"{symbol}{whole}"
            else:
                price_elem = element.select_one("span.a-price")
                if price_elem and price_elem.text.strip():
                    price = price_elem.text.strip()
                else:
                    # Fallback: any span containing a dollar sign
                    for pe in element.select("span"):
                        text = pe.text.strip()
                        if "$" in text:
                            price = text
                            break
            if price == "N/A":
                # Try meta price or data-attribute
                meta_price = element.get("data-price")
                if meta_price:
                    price = meta_price

            # Product rating - try more selectors and patterns
            rating = "N/A"
            rating_selectors = [
                "span.a-icon-alt",
                "i.a-icon-star-small span",
                "span.a-declarative .a-icon-alt",
                "span[aria-label*='out of 5 stars']",
            ]
            for sel in rating_selectors:
                rating_elem = element.select_one(sel)
                if rating_elem and rating_elem.text.strip():
                    rating = rating_elem.text.strip()
                    break

            # Product URL - more robust extraction
            product_url = "N/A"
            url_elem = element.select_one("h2 a")
            if url_elem and url_elem.get("href"):
                href = url_elem.get("href")
                product_url = href if href.startswith("http") else "https://www.amazon.com" + href
            else:
                link = element.select_one("a.a-link-normal.a-text-normal") or element.select_one("a.a-link-normal")
                if link and link.get("href"):
                    href = link.get("href")
                    product_url = href if href.startswith("http") else "https://www.amazon.com" + href

            # Stock status - best-effort from snippet text
            element_text = element.get_text(separator=" ").lower()
            in_stock = False
            if "in stock" in element_text or "available" in element_text or "prime" in element_text:
                in_stock = True

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
