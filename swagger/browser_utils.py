"""
Browser Utilities - Reusable methods for browser operations
"""

import logging
from playwright.sync_api import sync_playwright, Page, Browser

logging.basicConfig(
    level=logging.INFO,
    format='\n%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class BrowserUtils:
    """Reusable browser utility class for Playwright operations"""

    def __init__(self):
        self.playwright = None
        self.browser: Browser = None
        self.page: Page = None

    def launch_browser(self, headless: bool = False) -> Page:
        """
        Launch Chrome browser and create a new page.

        Args:
            headless: Run browser in headless mode (default: False)

        Returns:
            Page: Playwright page object
        """
        logger.info("=" * 60)
        logger.info("Launching Chrome Browser")
        logger.info(f"Headless Mode: {headless}")
        logger.info("=" * 60)

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            channel="chrome"
        )
        self.page = self.browser.new_page()

        logger.info("✅ Browser launched successfully")
        return self.page

    def navigate_to_url(self, url: str, wait_until: str = "networkidle") -> None:
        """
        Navigate to a URL.

        Args:
            url: The URL to navigate to
            wait_until: Wait condition ('load', 'domcontentloaded', 'networkidle')
        """
        if not self.page:
            raise Exception("Browser not launched. Call launch_browser() first.")

        logger.info("-" * 40)
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until=wait_until)

        logger.info(f"Page Title: {self.page.title()}")
        logger.info(f"Page URL: {self.page.url}")

    def close_browser(self) -> None:
        """Close the browser and cleanup resources."""
        logger.info("-" * 40)
        logger.info("Closing browser...")

        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

        self.page = None
        self.browser = None
        self.playwright = None

        logger.info("✅ Browser closed successfully")