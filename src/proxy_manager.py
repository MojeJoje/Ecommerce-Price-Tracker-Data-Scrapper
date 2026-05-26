"""Proxy management for rotating proxies across requests."""

import random
from typing import List, Optional


class ProxyManager:
    """Manages rotating proxies for web scraping."""

    def __init__(self, proxy_list: Optional[List[str]] = None):
        """
        Initialize ProxyManager.

        Args:
            proxy_list: List of proxy URLs to rotate through
        """
        self.proxy_list = proxy_list or []
        self.current_index = 0

    def add_proxy(self, proxy: str) -> None:
        """Add a proxy to the rotation list."""
        if proxy not in self.proxy_list:
            self.proxy_list.append(proxy)

    def add_proxies(self, proxies: List[str]) -> None:
        """Add multiple proxies to the rotation list."""
        for proxy in proxies:
            self.add_proxy(proxy)

    def get_next_proxy(self) -> Optional[str]:
        """Get the next proxy in rotation."""
        if not self.proxy_list:
            return None
        proxy = self.proxy_list[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxy_list)
        return proxy

    def get_random_proxy(self) -> Optional[str]:
        """Get a random proxy from the list."""
        if not self.proxy_list:
            return None
        return random.choice(self.proxy_list)

    def get_proxies_dict(self) -> Optional[dict]:
        """Get proxy dictionary for requests library."""
        proxy = self.get_next_proxy()
        if not proxy:
            return None
        return {
            "http": proxy,
            "https": proxy,
        }

    def remove_proxy(self, proxy: str) -> None:
        """Remove a proxy from the list."""
        if proxy in self.proxy_list:
            self.proxy_list.remove(proxy)

    def clear_proxies(self) -> None:
        """Clear all proxies."""
        self.proxy_list = []

    def __len__(self) -> int:
        """Return the number of proxies."""
        return len(self.proxy_list)
