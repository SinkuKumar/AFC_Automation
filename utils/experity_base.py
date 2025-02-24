import time
import logging
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
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

    def open_portal(self, url: str) -> None:
        """
        Opens the specified Experity portal URL.

        Args:
            url (str): URL of the Experity portal.

        Raises:
            ValueError: If the URL does not start with 'http://' or 'https://'.
            SeleniumException: If any other issue occurs during portal opening.
        """
        if not url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL format. Please include 'http://' or 'https://'.")
        
        try:
            self.driver.get(url)
            self.wait.until(page_loads)
            logging.info(f"Successfully opened Experity portal")

        except Exception as e:
            raise SeleniumException(f"Code: {em.PORTAL_ISSUE} | Message : Error while opening Experity portal")

    def login(self, username: str, password: str) -> None:
        """
        Automates the login process for Experity portal.

        Args:
            username (str): username to log in.
            password (str): password associated with the username.

        Returns:
            None

        Raises:
            SeleniumException: If any issue occurs during login process.
        """
        try:
            logging.info("Entering username.")
            login_username = self.wait.until(EC.element_to_be_clickable((By.ID,'txtLogin')))
            login_username.send_keys(username)

            logging.info("Clicking 'Next' button.")
            self.wait.until(EC.element_to_be_clickable((By.ID,'btnNext'))).click()

            logging.info("Entering password.")
            login_password = self.wait.until(EC.element_to_be_clickable((By.ID,'txtPassword')))
            login_password.send_keys(password)

            logging.info("Clicking 'Submit' button to log in.")
            self. wait.until(EC.element_to_be_clickable((By.ID,'btnSubmit'))).click()
            self.wait.until(page_loads)
            logging.info("Login process completed successfully.")

        except Exception as e:
            raise SeleniumException(f"Code: {em.INVALID_CREDENTIALS} | Message : Error in Logging process")
        
    def navigate_to_sub_nav(self, base_url: str, portal_url: str, sub_nav_item_name: str) -> None:
        """
        Navigates to a specific sub-navigation item on the Experity website.

        Args:
            base_url (str): The base URL of the website.
            portal_url (str): The specific portal or subdirectory in the URL.
            sub_nav_item_name (str): The name of the sub-navigation item to navigate to.

        Returns:
            None

        Raises:
            SeleniumException: If any issue occurs during navigating to sub nav item.
        """
        menu_mapping = {
            "Log Book": "LogBook",
            "Summary": "PatSummary",
            "Demographic": "PatInfo",
            "Payer/Insurance": "PatBilling",
            "Recievable": "PatAR",
            "Scan Documents": "BulkScanning",

            "Emp. Protocol": "CmpSearch",
            "Emp. Statement Review": "EmpStatementReview",
            "Occ Med Work Queue": "EPSWorkQueue",

            "Charge Entry": "CrgSummary",
            "Payment": "PymtBatch",
            "Fee Schedule": "FeeSchedule",
            "Managed Care": "ManagedCare",
            "Insurance": "InsSearch",
            "Documents": "DocList",
            "Billing Tasks": "Billing",
            "Work List": "WorkList",
            "Month End": "MonthEnd",
            "Patient Statements": "AutoPatStmt",
            "FirstData Admin": "FDManager",
            "Refunds Batch": "RefundsBatch",
            "Provider Search": "PhySearch",
            "Facility": "Facility",
            "Denials Management": "DenialsManagement",
            "Tools": "Tools",

            "Chart Review": "reviewworklist",
            "Reports": "Reports",
            "Statuses/Thresholds": "StatusThreshold",
            "Clinic": "ClinicInfo",
            "Primary Physician Info": "PrimPhySearch",
            "User Setup": "UserList",
            "SPU Emulation": "SPUEmulation",
            "Utility": "UtilList",
            "PatReminder": "PatReminder",
            "Group Security": "MenuOption",

            "Diagnosis Search": "DiagSearch",
            "Procedure Search": "ProcSearch",

            "Profile": "InfoProfile",

            "Home Page": "Announcement",
            "Educational Materials": "HelpDocument",
            # "Knowledge Base": "KnowledgeBase"
        }

        try:
            logging.info(f"Attempting to navigate to '{sub_nav_item_name}'.")
            if sub_nav_item_name not in menu_mapping:
                logging.error(f"Nav item '{sub_nav_item_name}' not found in menu mapping.")
                raise ValueError(f"Nav item '{sub_nav_item_name}' not found.")

            target_url = f"{base_url}/{portal_url}/{menu_mapping[sub_nav_item_name]}.aspx"
            self.driver.get(target_url)
            self.wait.until(page_loads)
            logging.info(f"Successfully navigated to '{sub_nav_item_name}'.")
        
        except Exception as e:
            raise SeleniumException(f"Code: {em.PORTAL_ISSUE} | Message : Error occurred while navigating to '{sub_nav_item_name}'.")
            
    def get_clinic_list(self) -> list:
        """
        Extracts and return data from 'Clinic List' table data.

        Args:
            None

        Returns:
            data(list): A list of lists containing table data where each inner list represents a row.

        Raises:
            SeleniumException: If any issue occurs during data extraction.
        """
        try:
            self.wait.until(page_loads)
            logging.info("Fetching page source.")
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            logging.info("Parsing HTML to find the table with id 'gvClinicList'.")
            table = soup.find('table', {'id': 'gvClinicList'})

            if table is None:
                raise SeleniumException("Table with id 'gvClinicList' not found.")

            data = []
            for row in table.find_all('tr'):
                cols = [col.get_text(strip=True) for col in row.find_all(['td', 'th'])]
                data.append(cols)

            logging.info("Data extraction successful.")
            return data

        except Exception as e:
            raise SeleniumException(f"Code: {em.DATA_FETCH_ISSUE} | Message : Error during data fetch.")
        
    def navigate_to_recievables_page(self, invoice_number: int) -> None:
        """
        Navigates to recievables page where recievables details are present.

        Args:
            invoice_number (int): The invoice_number to get recievables details.

        Returns:
            None

        Raises:
            SeleniumException: If any issue occurs during navigating to recievables page.
        """
        try:
            logging.info(f"Waiting for invoice number input field.")
            invoice_input = self.wait.until(EC.element_to_be_clickable((By.ID,'txtInvNum')))
            invoice_input.send_keys(invoice_number)
            invoice_input.send_keys(Keys.RETURN)
            logging.info(f"Input '{invoice_number}' invoice number submitted successfully.")

            self.wait.until(page_loads)
            patient_number_link = self.wait.until(EC.element_to_be_clickable((By.ID,'lbtnPatNum')))
            patient_number_link.click()
            logging.info("Patient number link clicked...")

            self.wait.until(page_loads)
            invoice_number_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="receivablesGridRow_{invoice_number}"]/td[1]/a')))
            invoice_number_link.click()
            self.wait.until(page_loads)
            logging.info('Invoice number link clicked...')
        except Exception as e:
            raise SeleniumException(f"Code: {em.PORTAL_ISSUE} | Message : Error in navigating to recievables page.")