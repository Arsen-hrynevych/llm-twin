from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BaseCrawler(ABC):
    """
    Abstract base class for crawlers that extract information from a web page.
    """

    @abstractmethod
    def extract_information(self, link: str, **kwargs) -> None:
        """
        Abstract method to extract information from a given URL.

        Args:
            link (str): The URL to scrape.
            **kwargs: Additional arguments for extraction.
        """
        ...


class BaseAbstractCrawler(BaseCrawler, ABC):
    """
    Base class for Selenium-based web crawlers.
    Configures WebDriver and provides methods for crawling and login.
    """

    def __init__(self) -> None:
        """
        Initializes the WebDriver with headless and performance options.
        """
        options = webdriver.ChromeOptions()

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-background-networking")
        options.add_argument("--ignore-certificate-errors")

        self.driver = webdriver.Chrome(options=options)

    def set_extra_driver_options(self, options: Options) -> None:
        """
        Placeholder to set extra WebDriver options in subclasses.

        Args:
            options (Options): The WebDriver options to set.
        """
        pass

    def login(self):
        """
        Placeholder method for login logic in subclasses.
        """
        pass
