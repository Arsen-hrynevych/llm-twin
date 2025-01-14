from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup

from core.config import settings
from core.exceptions import ImproperlyConfigured
from collecting_data_pipeline.crawlers.base import BaseAbstractCrawler


class LinkedInCrawler(BaseAbstractCrawler):
    def login(self):
        """
        Logs into LinkedIn using credentials from the settings.

        Raises:
            ImproperlyConfigured: If LinkedIn credentials are missing in settings.
        """
        self.driver.get(settings.LINKEDIN_LOGIN_URL)
        if not settings.LINKEDIN_USERNAME and not settings.LINKEDIN_PASSWORD:
            raise ImproperlyConfigured(
                "LinkedIn scraper requires an valid account to perform extraction"
            )

        self.driver.find_element(By.ID, "username").send_keys(
            settings.LINKEDIN_USERNAME
        )
        self.driver.find_element(By.ID, "password").send_keys(
            settings.LINKEDIN_PASSWORD
        )
        self.driver.find_element(
            By.CSS_SELECTOR, ".login__form_action_container button"
        ).click()

    def extract_information(self, link: str, **kwargs):
        self.login()

        soup = self._get_page_content(link)
        print(soup.prettify())

    def _get_page_content(self, url: str) -> BeautifulSoup:
        """Retrieve the page content of a given URL."""
        self.driver.get(url)
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.TAG_NAME, "body"))
        )
        return BeautifulSoup(self.driver.page_source, "html.parser")
