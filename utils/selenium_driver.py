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

    :param browser: The browser to use ('chrome', 'firefox', or 'edge').
    :type browser: str
    :param download_directory: The directory to download files to.
    :type download_directory: str, optional
    :param window_width: The width of the browser window.
    :type window_width: int, optional
    :param window_height: The height of the browser window.
    :type window_height: int, optional
    :param headless: Whether to run the browser in headless mode.
    :type headless: bool
    """
    BROWSER_OPTIONS = ['chrome', 'firefox', 'edge']

    def __init__(self, browser: str = 'chrome', download_directory: str = None, window_width: int = None, window_height: int = None, headless: bool = False) -> None:
        if browser not in self.BROWSER_OPTIONS:
            raise SeleniumException(f"(Error Code: {em.UNSUPPORTED_BROWSER}) :Unsupported browser. Please select from {self.BROWSER_OPTIONS}.")
        self.browser: str = browser
        self.download_directory: str = download_directory
        self.window_width = window_width
        self.window_height = window_height
        self.headless = headless
        self.driver: Optional[webdriver.Remote] = None

    def setup_driver(self) -> webdriver.Remote:
        """
        Set up and return the WebDriver instance based on the selected browser.

        :returns: WebDriver instance.
        :rtype: webdriver.Remote
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

        :returns: Chrome WebDriver instance.
        :rtype: webdriver.Chrome
        """
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-sync")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-component-update")
            options.add_argument("--enable-unsafe-swiftshader")
            options.add_argument("--disable-usb-keyboard-detect")
            options.add_argument("--disable-background-networking")
            options.add_argument("--disable-features=UseDeviceAsDictationMic")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--log-level=3")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            
            if self.headless:
                options.add_argument("--headless")

            prefs = {
                "download.default_directory": self.download_directory,
                "profile.default_content_settings.popups": 0,
                "profile.content_settings.exceptions.automatic_downloads.*.setting": 1
            }
            options.add_experimental_option("prefs", prefs)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            
            if self.window_width and self.window_height:
                options.add_argument(f"--window-size={self.window_width},{self.window_height}")
            else:
                options.add_argument("--start-maximized")

            self.driver = webdriver.Chrome(options=options)
            return self.driver
        except Exception:
            raise SeleniumException(f"Code: {em.BROWSER_INSTANCE_ISSUE} | Message: Unable to create Chrome Browser Instance")

    def setup_firefox(self) -> webdriver.Firefox:
        """
        Initialize and return a Firefox WebDriver instance with specified download settings.

        :returns: Firefox WebDriver instance.
        :rtype: webdriver.Firefox
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
            
            if self.headless:
                options.add_argument("--headless")
            
            if self.window_width and self.window_height:
                options.add_argument(f"--width={self.window_width}")
                options.add_argument(f"--height={self.window_height}")

            self.driver = webdriver.Firefox(options=options)
            
            if not (self.window_width and self.window_height):
                self.driver.maximize_window()
            return self.driver
        except Exception as e:
            raise SeleniumException(f"Code: {em.BROWSER_INSTANCE_ISSUE} | Message: Unable to create Firefox Browser Instance")

    def setup_edge(self) -> webdriver.Edge:
        """
        Initialize and return an Edge WebDriver instance with specified download settings.

        :returns: Edge WebDriver instance.
        :rtype: webdriver.Edge
        """
        try:
            options = EdgeOptions()
            prefs = {
                "download.default_directory": self.download_directory,
                "profile.default_content_settings.popups": 0,
                "profile.content_settings.exceptions.automatic_downloads.*.setting": 1
            }
            
            options.add_experimental_option("prefs", prefs)
            options.add_argument("--disable-blink-features=AutomationControlled")
            
            if self.headless:
                options.add_argument("--headless")
            
            if self.window_width and self.window_height:
                options.add_argument(f"--window-size={self.window_width},{self.window_height}")
            else:
                options.add_argument("--start-maximized")

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
            time.sleep(2)
            driver.quit()
        except Exception as e:
            print(e)
