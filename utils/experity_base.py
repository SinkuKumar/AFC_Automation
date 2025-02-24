import time
import logging
from datetime import datetime
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
            raise SeleniumException(f"Code: {em.NAVIGATION_FAILURE} | Message : Error occurred while navigating to '{sub_nav_item_name}'.")
            
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
        Navigates to recievables page where recievables details of given invoice number are present.

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
            raise SeleniumException(f"Code: {em.NAVIGATION_FAILURE} | Message : Error in navigating to recievables page.")

    def search_and_select_report(self, report_name: str) -> None:
        """
        Searches for a report by its name and selects it.

        Args:
            report_name(str): The name of the report to search and select.

        Returns:
            None

        Raises:
            SeleniumException: If any issue occurs during searching and selection of the report.
        """
        try:  
            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "reportMainWindow")))
            logging.info("Switched to 'reportMainWindow' iframe.")

            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "NavFrame")))
            self.wait.until(page_loads)
            logging.info("Switched to 'NavFrame' Frame.")
        except Exception as e:
            raise SeleniumException(f"Code: {em.NAVIGATION_FAILURE} | Message : Unable to switch to 'NavFrame' frame.")

        try:
            logging.info(f"Starting search for: {report_name}")
            self.wait.until(EC.visibility_of_element_located((By.NAME, "userSearch"))).clear()
            self.wait.until(EC.visibility_of_element_located((By.NAME, "userSearch"))).send_keys(report_name)

            logging.info("Clicking search button...")
            self.wait.until(EC.element_to_be_clickable((By.ID, 'dosearch'))).click()
            self.wait.until(page_loads)
            logging.info(f"Searched for report: {report_name}")
        except Exception as e:
            raise SeleniumException(f"Message : Unable to search for report.")

        try:
            self.driver.switch_to.default_content()
            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "reportMainWindow")))
            logging.info("Switched to 'reportMainWindow' iframe.")

            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "PVRC_MainStage")))
            logging.info("Switched to 'PVRC_MainStage' frame.")
            self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "//body"), f"Search for '{report_name}'"))
            self.wait.until(page_loads)
            self.wait.until(EC.element_to_be_clickable((By.ID, "mainbutton1"))).click()
            self.wait.until(page_loads)
            logging.info(f"Selected report: {report_name}")
        except Exception as e:
            raise SeleniumException(f"Message : Unable to select report after search.")

    def select_report_date_range(self, date1:str, date2:str) -> None:
        """
        Sets the 'From Service Date' and 'To Service Date'.
        
        Args:
            date1(str): One of the two dates entered by the user (Format: MM/DD/YYYY).
            date2(str): The other date entered by the user (Format: MM/DD/YYYY).
                        Either date may come first; the code will determine the start and end dates.
        
        Returns:
            None

        Raises:
            SeleniumException: If any issue occurs during searching and selection of the report.
        """
        date1_obj = datetime.strptime(date1, "%m/%d/%Y")
        date2_obj = datetime.strptime(date2, "%m/%d/%Y")

        from_date, to_date = (date1, date2) if date1_obj < date2_obj else (date2, date1)
        
        try:
            from_service_date = self.wait.until(EC.element_to_be_clickable((By.ID, 'FromServiceDate')))
            from_service_date.clear()
            from_service_date.send_keys(from_date)

            to_service_date = self.wait.until(EC.element_to_be_clickable((By.ID, 'ToServiceDate')))
            to_service_date.clear()
            to_service_date.send_keys(to_date)
        except Exception as e:
            raise SeleniumException(f"Code: {em.REPORT_FILTER_SELECTION_ERROR} | Message : Error during service date range selection.")

    def select_logbook_status(self, status_names: list) -> None:
        """
        Selects the specified logbook statuses.

        Args:
            status_name(list): A list of logbook status names to select.

        Returns:
            None

        Raises:
            SeleniumException: If any issue occurs during the logbook status names selection process.
        """
        status_mapping = {
            "All": 'freeStatusListcheck1',
            "Charged": 'freeStatusListcheck5'
        }

        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, 'freeunStatusListcheckall'))).click()
            logging.info("'Uncheck All' button clicked successfully.")

            for name in status_names:
                checkbox = self.wait.until(EC.element_to_be_clickable((By.ID, status_mapping[name])))
                if not checkbox.is_selected():
                    checkbox.click()
                    logging.info(f"Checkbox '{name}' selected.")
        except Exception as e:
            raise SeleniumException(f"Code: {em.REPORT_FILTER_SELECTION_ERROR} | Message : Error during logbook status selection.")

    def select_financial_class(self, class_names: list) -> None:
        """
        Selects the specified financial classes.

        Args:
            class_name(list): A list of financial class names to select.

        Returns:
            None

        Raises:
            SeleniumException: If any issue occurs during the financial class names selection process.
        """
        class_mapping = {
            "All": 'freePayerClasscheck1',
            "Great West": 'freePayerClasscheck5'
        }

        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, 'freeunPayerClasscheckall'))).click()
            logging.info("'Uncheck All' button clicked successfully.")

            for name in class_names:
                checkbox = self.wait.until(EC.element_to_be_clickable((By.ID, class_mapping[name])))
                if not checkbox.is_selected():
                    checkbox.click()
                    logging.info(f"Checkbox '{name}' selected.")
        except Exception as e:
            raise SeleniumException(f"Code: {em.REPORT_FILTER_SELECTION_ERROR} | Message : Error during financial class selection.")

    def select_arrival_status(self, status_names: list) -> None:
        """
        Selects the specified arrival statuses.

        Args:
            status_name(list): A list of arrival status names to select.

        Returns:
            None

        Raises:
            SeleniumException: If any issue occurs during the arrival status names selection process.
        """
        status_mapping = {
            "All": 'freeArrivalStatuscheck1',
            "At Home": 'freeArrivalStatuscheck5'
        }

        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, 'freeunArrivalStatuscheckall'))).click()
            logging.info("'Uncheck All' button clicked successfully.")

            for name in status_names:
                checkbox = self.wait.until(EC.element_to_be_clickable((By.ID, status_mapping[name])))
                if not checkbox.is_selected():
                    checkbox.click()
                    logging.info(f"Checkbox '{name}' selected.")
        except Exception as e:
            raise SeleniumException(f"Code: {em.REPORT_FILTER_SELECTION_ERROR} | Message : Error during arrival status selection.")

    def run_report(self) -> None:
        """
        Triggers the 'Run Report' action by clicking the designated 'Run Report' button.

        Args:
            None

        Returns:
            None

        Raises:
            SeleniumException: If any issue occurs while running the report.
        """
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @name='submitbtn' and @value='Run Report']"))).click()
            logging.info("'Run Report' button clicked successfully.")
        except Exception as e:
            raise SeleniumException(f"Message : Error occurred while clicking on 'Run Report' button.")

    def switch_to_report_window(self) -> None:
        """
        Switches the WebDriver to a new browser window that contains the report data.

        This method assumes that the new report window is the second window opened.

        Args:
            None

        Returns:
            None

        Raises:
            SeleniumException: If any issue occurs while switching to report window.
        """
        try:
            logging.info("Fetching available window handles.")
            new_window = [handle for handle in self.driver.window_handles][1]
            self.driver.switch_to.window(new_window)
            logging.info("Successfully switched to the report window.")
        except Exception as e:
            raise SeleniumException(f"Message : Error occurred while switching to report window.")
        
    # def download_report(self):
    #     self.wait.until(page_loads)
    #     self.wait.until(EC.element_to_be_clickable((By.ID, "ReportViewerControl_ctl05_ctl04_ctl00_ButtonImg")))
    #     csv_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, \"exportReport('XML')\") and normalize-space(text())='XML file with report data']")))

    def logout(self) -> None:
        """
        Logs out the user by clicking the logout button.

        Args:
            None

        Returns:
            None

        Raises:
            SeleniumException: If any issue occurs during logout.
        """
        try:
            self.driver.switch_to.default_content()
            logging.info("Attempting to locate the logout button...")
            logout_button = self.wait.until(EC.element_to_be_clickable((By.ID,'tdMenuBarItemlogout')))
            logout_button.click()
            self.wait.until(page_loads)
            logging.info("Logout successful.")
        except Exception as e:
            raise SeleniumException(f"Code: {em.LOGOUT_ISSUE} | Message : Error occurred during logout.")