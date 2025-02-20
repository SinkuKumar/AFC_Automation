"""
SeleniumDriver module provides a SeleniumDriver class that allows the user to select a browser (Chrome, Firefox, or Edge) and initialize the corresponding WebDriver.

Usage:
    selenium_base = SeleniumDriver(browser='chrome')
    driver = selenium_base.setup_driver()

Type Hints:
- `browser`: str - The name of the browser to use. Options: 'chrome', 'firefox', 'edge'.

Browser Selection Guide:
- Use 'chrome' for most testing purposes due to its popularity and extensive support.
- Use 'firefox' when you need to test on Mozilla Firefox.
- Use 'edge' when testing Microsoft Edge-specific functionality.

Note:
- WebDriver will be installed automatically using the `webdriver_manager` package.

:Date: Feb 13, 2025
:Version: 1.0
:Author: Sinku Kumar
"""

import os
import sys
from typing import Optional

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import error_messages as em
from utils.automation_exceptions import SeleniumException 

class SeleniumDriver:
    """
    SeleniumDriver class for setting up Selenium WebDriver instances with multiple browsers.

    This class provides methods to initialize WebDriver instances for Chrome, Firefox, and Edge browsers,
    with support for specifying a default download directory and disabling download prompts.
    """
    BROWSER_OPTIONS = ['chrome', 'firefox', 'edge']

    def __init__(self, browser: str = 'chrome', download_directory: str = None) -> None:
        """
        Initialize the SeleniumDriver with a specified browser and download directory.

        :param browser: The browser to use ('chrome', 'firefox', or 'edge').
        :param download_directory: The directory to download files to.
        """
        if browser not in self.BROWSER_OPTIONS:
            raise SeleniumException(f"(Error Code: {em.UNSUPPORTED_BROWSER}) :Unsupported browser. Please select from {self.BROWSER_OPTIONS}.")
        self.browser: str = browser
        self.download_directory: str = download_directory
        self.driver: Optional[webdriver.Remote] = None

    def setup_driver(self) -> webdriver.Remote:
        """
        Set up and return the WebDriver instance based on the selected browser.

        :return: WebDriver instance.
        """
        try:
            if self.browser == 'chrome':
                return self.setup_chrome()
            elif self.browser == 'firefox':
                return self.setup_firefox()
            elif self.browser == 'edge':
                return self.setup_edge()
        except Exception as e:
            raise SeleniumException(f"Error setting up the WebDriver: {e}")

    def setup_chrome(self) -> webdriver.Chrome:
        """
        Initialize and return a Chrome WebDriver instance with specified download settings.

        :return: Chrome WebDriver instance.
        """
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            prefs = {
                "download.default_directory": self.download_directory,
                "profile.default_content_settings.popups": 0,
                "profile.content_settings.exceptions.automatic_downloads.*.setting": 1
            }
            options.add_experimental_option("prefs", prefs)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self.driver = webdriver.Chrome(options=options)
            return self.driver
        except Exception as e:
            raise SeleniumException(f"Code: {em.BROWSER_INSTANCE_ISSUE} | Message: Unable to create Chrome Browser Instance")

    def setup_firefox(self) -> webdriver.Firefox:
        """
        Initialize and return a Firefox WebDriver instance with specified download settings.

        :return: Firefox WebDriver instance.
        """
        try:
            options = FirefoxOptions()
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.dir", self.download_directory)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf, application/octet-stream")
            options.set_preference("browser.download.manager.showWhenStarting", False)
            options.set_preference("browser.helperApps.alwaysAsk.force", False)
            options.set_preference("dom.webdriver.enabled", False)
            options.set_preference("dom.webnotifications.enabled", False)
            self.driver = webdriver.Firefox(options=options)
            return self.driver
        except Exception as e:
            raise SeleniumException(f"Code: {em.BROWSER_INSTANCE_ISSUE} | Message: Unable to create Firefox Browser Instance")

    def setup_edge(self) -> webdriver.Edge:
        """
        Initialize and return an Edge WebDriver instance with specified download settings.

        :return: Edge WebDriver instance.
        """
        try:
            options = EdgeOptions()
            prefs = {
                "download.default_directory": self.download_directory,
                "profile.default_content_settings.popups": 0,
                "profile.content_settings.exceptions.automatic_downloads.*.setting": 1
            }
            options.add_experimental_option("prefs", prefs)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_argument("--disable-blink-features=AutomationControlled")
            self.driver = webdriver.Edge(options=options)
            return self.driver
        except Exception as e:
            raise SeleniumException(f"Code: {em.BROWSER_INSTANCE_ISSUE} | Message: Unable to create Edge Browser Instance")


if __name__ == '__main__':
    # Example usage
    import os
    import time
    
    browsers = ['chrome', 'firefox', 'edge']
    download_directory = os.getcwd()

    for browser in browsers:
        try:
            selenium = SeleniumDriver(browser=browser, download_directory=download_directory)
            driver = selenium.setup_driver()
            driver.get("https://www.google.com")
            time.sleep(5)
            driver.quit()
        except Exception as e:
            print(e)
