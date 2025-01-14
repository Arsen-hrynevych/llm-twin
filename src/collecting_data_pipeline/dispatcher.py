import re
import logging
from typing import Type

from collecting_data_pipeline.crawlers.base import BaseCrawler


logger = logging.getLogger(__name__)


class CrawlerDispatcher:
    """
    A dispatcher that manages and routes URLs to appropriate crawler implementations.

    This class maintains a registry of domain-specific crawlers and matches incoming URLs
    to their corresponding crawler implementations.
    """

    def __init__(self) -> None:
        self._crawlers = {}

    def register(self, domain: str, crawler: Type[BaseCrawler]) -> None:
        """
        Register a crawler for a specific domain.

        Args:
            domain (str): The domain name without protocol or www prefix (e.g., 'example')
            crawler (Type[BaseCrawler]): The crawler class to handle URLs from this domain

        Raises:
            ValueError: If domain is empty or invalid
            TypeError: If crawler is not a subclass of BaseCrawler
        """
        if not domain or not isinstance(domain, str):
            raise ValueError("Domain must be a non-empty string")

        if not isinstance(crawler, type) or not issubclass(crawler, BaseCrawler):
            raise TypeError("Crawler must be a subclass of BaseCrawler")

        pattern = re.compile(
            r"^https://(www\.)?{domain}\.com/.*$".format(domain=re.escape(domain)),
            re.IGNORECASE,
        )
        self._crawlers[pattern] = crawler
        logger.info(
            f"Registered crawler {crawler.__name__} for domain pattern: {pattern.pattern}"
        )

    def get_crawler(self, url: str) -> "BaseCrawler":
        """
        Get the appropriate crawler instance for the given URL.

        Args:
            url (str): The URL to find a crawler for

        Returns:
            Optional[BaseCrawler]: An instance of the matching crawler class,
                                 or None if no matching crawler is found

        Raises:
            ValueError: If the URL is empty or malformed
        """
        if not url or not isinstance(url, str):
            raise ValueError("URL must be a non-empty string")

        try:
            for pattern, crawler_cls in self._crawlers.items():
                if re.match(pattern, url):
                    return crawler_cls()

            logger.warning(f"No crawler found for URL: {url}")
            return None
        except Exception as exc:
            logger.error(f"Error processing URL {url}: {str(exc)}")
            raise
