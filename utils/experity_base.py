import time
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .exception_usage import SeleniumException
from utils import error_messages as em

def page_loads(driver: WebDriver) -> bool:
    """
    Checks if the web page has fully loaded by verifying document.readyState.

    Args:
        driver (WebDriver): Selenium WebDriver instance controlling the browser.

    Returns:
        bool: True if the page is fully loaded, False otherwise.

    """
    return driver.execute_script("return document.readyState") == "complete"

class ExperityBase:
    def __init__(self, webdriver: WebDriver, time_out: int = 100):
        self.driver = webdriver
        self.time_out = time_out
        self.wait = WebDriverWait(webdriver, self.time_out)

    def open_portal(self, url: str):
        """
        Opens the specified Experity portal URL.

        Args:
            url (str): URL of the Experity portal.

        Raises:
            ValueError: If the URL does not start with 'http://' or 'https://'.
        """
        if not url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL format. Please include 'http://' or 'https://'.")
        
        try:
            self.driver.get(url)
            logging.info(f"Successfully opened Experity portal")

        except Exception as e:
            raise SeleniumException(f"Code: {em.PORTAL_ISSUE} | Message : Error while opening Experity portal")

    def login(self, username: str, password: str):
        """
        Automates the login process for Experity portal.

        Args:
            username (str): username to log in.
            password (str): password associated with the username.

        Returns:
            None
        """
        try:
            logging.info("Entering username.")
            login_username = self.wait.until(EC.element_to_be_clickable((By.ID,'txtLogin')))
            login_username.send_keys(username)

            logging.info("Clicking 'Next' button.")
            self.driver.find_element(By.ID,'btnNext').click()

            logging.info("Entering password.")
            login_password = self.wait.until(EC.element_to_be_clickable((By.ID,'txtPassword')))
            login_password.send_keys(password)

            logging.info("Clicking 'Submit' button to log in.")
            self. wait.until(EC.element_to_be_clickable((By.ID,'btnSubmit'))).click()
            logging.info("Login process completed successfully.")

        except Exception as e:
            raise SeleniumException(f"Code: {em.INVALID_CREDENTIALS} | Message : Error in Logging process")
     