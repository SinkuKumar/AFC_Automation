import os
import sys
import time
import logging
from functools import wraps
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from utils.file_folder import create_directories

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import error_messages as em
from utils.automation_exceptions import SeleniumException
TIMESTAMP_IDENTIFIER = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def page_loads(driver: WebDriver) -> bool:
    """
    Checks if the web page has fully loaded by verifying document.readyState.

    :param driver: Selenium WebDriver instance controlling the browser.
    :type driver: WebDriver
    :returns: True if the page is fully loaded, False otherwise.
    :rtype: bool

    :raises None:
    """
    return driver.execute_script("return document.readyState") == "complete"

def retry_on_exception(retries: int = 3, delay: int = 2) -> callable:
    """
    Decorator to automatically retry a class method if it raises an exception.

    :param retries: The number of retry attempts before failing completely.
    :type retries: int
    :param delay: The wait time (in seconds) between retries.
    :type delay: int
    :returns: A wrapped function with retry logic applied.
    :rtype: Callable

    :raises SeleniumException: If the function still fails after all retries.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logging.warning(f"Retry {attempts}/{retries} for {func.__name__} failed: {e}")
                    time.sleep(delay)
            raise SeleniumException(f"Message : {func.__name__} failed after {retries} retries.")
        return wrapper
    return decorator

def switch_to_latest_window(driver: WebDriver) -> None:
    """
    Switches the Selenium WebDriver's focus to the latest (most recently opened) browser window.

    This function waits until at least two windows are open and then switches the driver's focus
    to the latest window.

    :param driver: The Selenium WebDriver instance controlling the browser.
    :type driver: WebDriver

    :return: None

    :raises SeleniumException: If any issue occurs while switching to latest window.
    """
    logging.info("Attempting to switch to the latest browser window.")

    try:
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        latest_handle = driver.window_handles[-1]

        driver.switch_to.window(latest_handle)
        logging.info(f"Switched to the latest window: {latest_handle}")

    except Exception as e:
        raise SeleniumException(f"Message : Error occurred while switching to latest window.")

class ExperityBase:
    def __init__(self, webdriver: WebDriver, time_out: int = 100):
        self.driver = webdriver
        self.time_out = time_out
        self.wait = WebDriverWait(webdriver, self.time_out)

    @retry_on_exception()
    def open_portal(self, url: str) -> None:
        """
        Opens the specified Experity portal URL.

        :param url: URL of the Experity portal.
        :type url: str

        :raises ValueError: If the URL does not start with 'http://' or 'https://'.
        :raises SeleniumException: If any other issue occurs during portal opening.
        """
        if not url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL format. Please include 'http://' or 'https://'.")
        
        try:
            self.driver.get(url)
            self.wait.until(page_loads)
            logging.info(f"Successfully opened Experity portal")

        except Exception as e:
            raise SeleniumException(f"Code: {em.PORTAL_ISSUE} | Message : Error while opening Experity portal")
    
    @retry_on_exception()
    def experity_version(self) -> str:
        """
        Extract the portal URL segment from the current browser URL.

        This method fetches the current URL from the WebDriver, splits it by slashes (`/`),
        and returns the 4th part (index 3), which is the portal url/segment.
        :returns: portal_url: The portal URL segment extracted from the current browser URL.
        :rtype: str

        :raises ValueError: If the URL structure does not match the expected format.
        :raises SeleniumException: If any other issue occurs while extracting portal URL segment.
        """
        try:
            current_url = self.driver.current_url
            logging.info(f"Current URL fetched from driver: {current_url}")

            url_parts = current_url.split('/')
            if len(url_parts) < 4:
                raise ValueError(f"Unexpected URL structure: {current_url}")

            portal_url = url_parts[3]
            logging.info(f"Extracted portal URL segment: {portal_url}")
            return portal_url

        except Exception as e:
            raise SeleniumException(f"Code: {em.PORTAL_ISSUE} | Message : Error while extracting portal URL segment.")

    def login(self, username: str, password: str) -> None:
        """
        Automates the login process for Experity portal, checks for invalid username or password..

        :param username: username to log in.
        :type username: str
        :param password: password associated with the username.
        :type password: str
        :returns: None

        :raises SeleniumException: If any issue occurs during login process.
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
            self.wait.until(EC.element_to_be_clickable((By.ID,'btnSubmit'))).click()
            self.wait.until(page_loads)

            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            screenshots_folder = os.path.join(project_root, "Screenshots")
            create_directories([screenshots_folder])
            self.wait.until(page_loads)
            if self.driver.title == "PVM > Login":
                """
                Verify if the username or password is incorrect, and capture a screenshot if necessary.
                """
                if self.driver.find_element(By.ID, "lblErrorMessage").text == "Invalid User Credentials":
                    screenshot_path = os.path.join(screenshots_folder, f"Invalid_User_Cred_{username}_{TIMESTAMP_IDENTIFIER}.png")
                    self.driver.find_element(By.ID, "ctl00").screenshot(screenshot_path)
                    raise Exception("Invalid user credentials.")

            elif self.driver.title == "PVM > User Profile":
                """
                Check if the user is required to change the password, and capture a screenshot if necessary.
                """
                try:
                    error_message = self.driver.find_element(By.ID, "lblPasswordError").text
                except:
                    error_message = ""

                if error_message == "You are required to change your password.":
                    screenshot_path = os.path.join(screenshots_folder, f"Password_Change_{username}_{TIMESTAMP_IDENTIFIER}.png")
                    self.driver.find_element(By.ID, "pnlPassword").screenshot(screenshot_path)
                    raise Exception("Password change required")

                elif "Your password is about to expire on" in error_message:
                    screenshot_path = os.path.join(screenshots_folder, f"Password_Expire_{username}_{TIMESTAMP_IDENTIFIER}.png")
                    self.driver.find_element(By.ID, "pnlPassword").screenshot(screenshot_path)
                    logging.warning(error_message)

            logging.info("Login process completed successfully.")

        except Exception as e:
            raise SeleniumException(f"Code: {em.INVALID_CREDENTIALS} | Message : Error in Logging process - {str(e)}")

    def navigate_to(self, base_url: str, portal_url: str, sub_nav_item_name: str) -> None:
        """
        Navigates to a specific sub-navigation item on the Experity website.

        :param base_url: The base URL of the website.
        :type base_url: str
        :param portal_url: The specific portal or subdirectory in the URL.
        :type portal_url: str
        :param sub_nav_item_name: The name of the sub-navigation item to navigate to.
        :type sub_nav_item_name: str
        :returns: None

        :raises SeleniumException: If any issue occurs during navigating to sub nav item.
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

    def search_and_select_report(self, report_name: str) -> None:
        """
        Searches for a report by its name and selects it.

        :param report_name: The name of the report to search and select.
        :type report_name: str
        :returns: None

        :raises SeleniumException: If any issue occurs during searching and selection of the report.
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
        Sets the 'From Service Date' and 'To Service Date' fields in a web form.

        This method determines the correct order of the provided dates and inputs them
        into the respective fields on the web page. It waits for the fields to be clickable
        before interacting with them.

        :param date1: The first date entered by the user (Format: MM/DD/YYYY).
        :type date1: str
        :param date2: The second date entered by the user (Format: MM/DD/YYYY).
                      Either date may come first; the method will determine the correct order.
        :type date2: str

        :raises SeleniumException: If an error occurs during the interaction with the web elements.
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

    def select_month(self, month: str = None, from_month: str = None, to_month: str = None):
        """
        Selects a single month or a month range (from_month to to_month).

        This function interacts with Selenium dropdowns to either:
        - Select a single month from the "ClosingDate" dropdown.
        - Select a date range using the "FromClosingDate" and "ToClosingDate" dropdowns.

        Date Format:
            Month Year (e.g., 'March 2010', 'December 2022')

        :param month: Single month to select.
        :type month: str, optional
        :param from_month: Start month for range selection.
        :type from_month: str, optional
        :param to_month: End month for range selection.
        :type to_month: str, optional
        :returns: None
        :rtype: None

        :raises ValueError: If arguments provided are invalid (e.g., only from_month or to_month is given).
        :raises SeleniumException: If any issue occurs during searching and selection of the report.
        """
        try:
            self.driver.switch_to.default_content()
            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "reportMainWindow")))
            logging.info("Switched to 'reportMainWindow' iframe.")

            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "PVRC_MainStage")))
            logging.info("Switched to 'PVRC_MainStage' frame.")
           
            if month:
                logging.info(f"Selecting month: {month}")
                month_dropdown = self.wait.until(EC.visibility_of_element_located((By.NAME, "ClosingDate")))
                Select(month_dropdown).select_by_visible_text(month)
                logging.info(f"Successfully selected month: {month}")

            elif from_month and to_month:
                logging.info(f"Selecting month range: {from_month} to {to_month}")

                from_dropdown = self.wait.until(EC.visibility_of_element_located((By.NAME, "FromClosingDate")))
                Select(from_dropdown).select_by_visible_text(from_month)

                to_dropdown = self.wait.until(EC.visibility_of_element_located((By.NAME, "ToClosingDate")))
                Select(to_dropdown).select_by_visible_text(to_month)

                logging.info(f"Successfully selected month range: {from_month} to {to_month}")

            else:
                raise ValueError("Arguments provided are invalid for range selection.")
        except Exception as e:
            raise SeleniumException(f"Code: {em.REPORT_FILTER_SELECTION_ERROR} | Message : Failed to select month(s).")

    def select_logbook_status(self, status_names: list) -> None:
        """
        Selects the specified logbook statuses.

        :param status_name: A list of logbook status names to select.
        :type status_name: list
        :returns: None

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
            self.wait.until(page_loads)

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

        :param class_name: A list of financial class names to select.
        :type class_name: list
        :returns: None

        :raises SeleniumException: If any issue occurs during the financial class names selection process.
        """
        class_mapping = {
            "All": 'freePayerClasscheck1',
            "Great West": 'freePayerClasscheck5'
        }

        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, 'freeunPayerClasscheckall'))).click()
            logging.info("'Uncheck All' button clicked successfully.")
            self.wait.until(page_loads)

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

        :param status_name: A list of arrival status names to select.
        :type status_name: list
        :returns: None

        :raises: SeleniumException: If any issue occurs during the arrival status names selection process.
        """
        status_mapping = {
            "All": 'freeArrivalStatuscheck1',
            "At Home": 'freeArrivalStatuscheck5'
        }

        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, 'freeunArrivalStatuscheckall'))).click()
            logging.info("'Uncheck All' button clicked successfully.")
            self.wait.until(page_loads)

            for name in status_names:
                checkbox = self.wait.until(EC.element_to_be_clickable((By.ID, status_mapping[name])))
                if not checkbox.is_selected():
                    checkbox.click()
                    logging.info(f"Checkbox '{name}' selected.")
        except Exception as e:
            raise SeleniumException(f"Code: {em.REPORT_FILTER_SELECTION_ERROR} | Message : Error during arrival status selection.")

    def select_date_type(self, date_type: str) -> None:
        """
        Selects the specified Date type.

        :param date_type: Date type to select.
        :type date_type: str
        :returns: None

        :raises: SeleniumException: If any issue occurs during the arrival status names selection process.
        """
        try:
            date_type_radio_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"div#rightcol input[type='radio'][value='{date_type}']")))
            date_type_radio_button.click()
            logging.info(f"{date_type} radio button clicked successfully.")
        except Exception as e:
            raise SeleniumException(f"Code: {em.REPORT_FILTER_SELECTION_ERROR} | Message : Error during 'Date Type' selection.")

    def uncheck_all_check_all(self, uncheck_button_identifier_id: str, check_checkbox_identifier_id: str):
        """
        Performs the action of first clicking the 'Uncheck All' button and then selecting the 'All' checkbox.

        This is a 'fallback method' meant for scenarios where dedicated filter selection methods 
        (like `select_logbook_status`, `select_financial_class`, etc.) are not implemented for a particular filter.

        Note:
            - Prefer using dedicated methods like `select_logbook_status`, `select_financial_class`, etc., which are more maintainable and easier to enhance.
            - Use this method only when no dedicated method exists, or the filter is generic and does not have structured helper methods yet.
            - This method directly interacts with the UI elements via their IDs, so ensure the identifiers are correct.
        
        :params uncheck_button_identifier_id: The HTML element ID for the 'Uncheck All' button.
        :type uncheck_button_identifier_id: str
        :param check_checkbox_identifier_id: The HTML element ID for the 'All' checkbox.
        :type check_checkbox_identifier_id: str
        :returns: None

        :raises SeleniumException: If any issue occurs while clicking the 'Uncheck All' button and then selecting the 'All' checkbox.
        """

        logging.info(f"Starting 'Uncheck All' and 'Check All' process using elements.")

        try:
            uncheck_button = self.wait.until(EC.element_to_be_clickable((By.ID, uncheck_button_identifier_id)))
            uncheck_button.click()
            logging.info(f"Clicked 'Uncheck All' button (ID: {uncheck_button_identifier_id}).")

            self.wait.until(page_loads)

            check_checkbox = self.wait.until(EC.element_to_be_clickable((By.ID, check_checkbox_identifier_id)))
            if not check_checkbox.is_selected():
                check_checkbox.click()
                logging.debug(f"Checked the 'All' checkbox (ID: {check_checkbox_identifier_id}).")
            else:
                logging.debug(f"'All' checkbox was already selected (ID: {check_checkbox_identifier_id}).")

            logging.info("Successfully clicked on 'Uncheck All' and selected 'All' checkbox.")
        
        except Exception as e:
            raise SeleniumException(f"Code: {em.REPORT_FILTER_SELECTION_ERROR} | Message: Unable to click 'Uncheck All' and select 'All' checkbox.")

    def include_x_rays_reviewed(self):
        """
        Performs the action of clicking the `Include x-rays in 'reveiwed' status` button.
        This method is used for XRY_03 reports.
        """
        try:
            review_button = self.wait.until(EC.element_to_be_clickable((By.NAME, 'freeIncludeReviewedStatus' )))
            review_button.click()
            logging.info("Clicked include x-rays in reveiwed status button.")
        except Exception as e:
            raise SeleniumException(f"Code: {em.REPORT_FILTER_SELECTION_ERROR} | Message: Unable to click include x-rays in reveiwed status button.")

    @retry_on_exception()
    def select_pm_report(self, category_name: str, subcategory_name: str, report_identifier: str) -> None:
        """
        This function handles:
        1. Expanding the correct Category (by name)
        2. Expanding the correct Subcategory (by name), scoped inside the Category
        3. Clicking the correct Report (by report code or report name), scoped inside the Subcategory

        :param category_name: Name of the Category.
        :type category_name: str
        :param subcategory_name: Name of the Subcategory.
        :type subcategory_name: str
        :param report_identifier: Either the report name OR report code.
        :type report_identifier: str
        :returns: None

        :raises SeleniumException: If any issue occurs during the pm report selection process.
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
            month_end_button = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@id='monthend' and .//b[text()='Month End Only']]")))
            month_end_button.click()

            tree_container = self.wait.until(EC.presence_of_element_located((By.ID, "treecontainer1x0x0x0")))

            category_div = self.wait.until(lambda d: tree_container.find_element(
                By.XPATH, f".//div[contains(@id, 'treeitem') and .//b[text()='{category_name}']]"
            ))
            category_expand_img = self.wait.until(lambda d: category_div.find_element(
                By.XPATH, ".//div[contains(@id, 'treeimg')]//img"
            ))
            category_expand_img.click()

            subcategory_div = self.wait.until(lambda d: category_div.find_element(
                By.XPATH, f".//following-sibling::div//div[contains(@id, 'treeitem') and .//b[text()='{subcategory_name}']]"
            ))

            subcategory_expand_img = subcategory_div.find_element(By.XPATH, ".//div[contains(@id, 'treeimg')]//img")
            subcategory_expand_img.click()

            subcategory_container = subcategory_div.find_element(By.XPATH, "./following-sibling::div[contains(@id, 'treecontainer')]")

            report_div = self.wait.until(lambda d: subcategory_container.find_element(
                By.XPATH, f".//div[contains(@class, 'treeitem') and (contains(., '{report_identifier}'))]"
            ))
            report_div.click()
            time.sleep(2)
        except:
            raise SeleniumException(f"Message : Error while selecting report '{report_identifier}'.")

        try:
            self.driver.switch_to.default_content()
            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "reportMainWindow")))
            logging.info("Switched to 'reportMainWindow' iframe.")

            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "PVRC_MainStage")))
            self.wait.until(page_loads)
            logging.info("Switched to 'PVRC_MainStage' frame.")

            breadcrumb_locator = (By.CSS_SELECTOR, "#adivname > div:first-child")
            self.wait.until(EC.visibility_of_element_located(breadcrumb_locator))

        except Exception as e:
            raise SeleniumException(f"Code: {em.NAVIGATION_FAILURE} | Message : Unable to switch to 'PVRC MainStage' frame.")

    def select_pm_report_filter(self, report_code: str, cls_from_month: str = None, cls_to_month: str = None, cls_month_end: str = None, serv_from_date: str = None, serv_to_date: str = None, rev_code: str = None, report_type: str = None) -> None:
        """
        Applies filters to select a PM report based on various criteria.

        :param report_code: The code identifying the specific report to be selected.
        :type report_code: str
        :param cls_from_month: From month for the closing date filter (format: "Month YYYY"). Defaults to None.
        :type cls_from_month: str, optional
        :param cls_to_month: To month for the closing date filter (format: "Month YYYY"). Defaults to None.
        :type cls_to_month: str, optional
        :param cls_month_end: Closing month-end date filter (format: "Month YYYY"). Defaults to None.
        :type cls_month_end: str, optional
        :param serv_from_date: From date for the service date filter (format: "MM/DD/YYYY"). Defaults to None.
        :type serv_from_date: str, optional
        :param serv_to_date: To date for the service date filter (format: "MM/DD/YYYY"). Defaults to None.
        :type serv_to_date: str, optional
        :param rev_code: Revenue code filter. Defaults to None.
        :type rev_code: str, optional
        :param report_type: Type of report being requested. Defaults to None.
        :type report_type: str, optional
        :returns: None

        :raises SeleniumException: If any issue occurs during PM report filter selection process. 

        Notes:
            This function is intended to apply various filters that refine the selection of a PM report.
        """
        try:
            if report_code in ["ADJ 0", "AGE 11 DW", "AGE 12 DW", "ARC 3 DW", "REV 1 DW", "REV 15", "REV 20 DW"]:
                dates = [cls_from_month, cls_to_month]
                cls_from_month, cls_to_month = sorted(dates, key=lambda x: datetime.strptime(x, "%B %Y"))

                self.select_month(from_month=cls_from_month, to_month=cls_to_month)
                if report_code in ["ARC 3 DW", "ARC 4 DW", "REV 20 DW"]:

                    self.wait.until(EC.element_to_be_clickable((By.ID, 'freeunClinicscheckall'))).click()
                    logging.info("'Uncheck All' button clicked successfully.")

                    checkbox = self.wait.until(EC.element_to_be_clickable((By.ID, 'freeClinicscheck1')))
                    if not checkbox.is_selected():
                        checkbox.click()
                        logging.info(f"Checkbox 'ALL' selected.")
                        
                    if report_code in ["ARC 3 DW"]:
                        self.wait.until(EC.element_to_be_clickable((By.ID, 'freeunPayerClasscheckall'))).click()
                        logging.info("'Uncheck All' button clicked successfully.")

                        checkbox = self.wait.until(EC.element_to_be_clickable((By.ID, 'freePayerClasscheck1')))
                        if not checkbox.is_selected():
                            checkbox.click()
                            logging.info(f"Checkbox 'ALL' selected.")

                    elif report_code in ["REV 20 DW"]:
                        type = self.wait.until(EC.visibility_of_element_located((By.NAME, "BranchingDDL")))
                        Select(type).select_by_visible_text(report_type)

            elif report_code in ["PAT 0",  "PAY 5", "MRI 2"]:
                self.select_report_date_range(serv_from_date, serv_to_date)
            elif report_code in ["AGE 13 DW"]:
                pass
            else:
                self.select_month(month=cls_month_end)
                if report_code in ["REV 14"]:
                    revenue_code = self.wait.until(EC.visibility_of_element_located((By.NAME, "freeRevCode")))
                    Select(revenue_code).select_by_visible_text(rev_code)

        except Exception as e:
            raise SeleniumException("Message : Error occurred while selecting pm report filters.")

    def get_clinic_list(self) -> list:
        """
        Extracts and return data from 'Clinic List' table data.

        :returns: A list of lists containing table data where each inner list represents a row.
        :rtype: data(list)

        :raises SeleniumException: If any issue occurs during data extraction.
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

        :parma invoice_number: The invoice_number to get recievables details.
        :type invoice_numer: int
       :returns: None

        :raises SeleniumException: If any issue occurs during navigating to recievables page.
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

    def run_report(self) -> None:
        """
        Triggers the 'Run Report' action by clicking the designated 'Run Report' button.

        :returns: None

        :raises SeleniumException: If any issue occurs while running the report.
        """
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @name='submitbtn' and @value='Run Report']"))).click()
            logging.info("'Run Report' button clicked successfully.")
        except Exception as e:
            raise SeleniumException(f"Message : Error occurred while clicking on 'Run Report' button.")
        
    def download_report(self, report_format:str) -> None:
        """
        Automates the process of downloading a report in provided report format.

        Steps:
        1. Switches to the latest browser window.
        2. Waits for the page to fully load.
        3. Ensures that the report viewer is ready.
        4. Selects and clicks the provided report format download option.

        :param report_format: Specifies the format of the report (e.g., 'CSV', 'Excel', 'TXT').
        :type report_format: str
        :returns: None

        :raises SeleniumException: If any issue occurs during report download.
        """

        format_mapping = {
            "XML": {
                "onclick": 'XML',
                "text": 'XML file with report data'
            },
            "CSV": {
                "onclick": 'CSV',
                "text": 'CSV (comma delimited)'
            },
            "PDF": {
                "onclick": 'PDF',
                "text": 'PDF'
            },
            "MHTML": {
                "onclick": 'MHTML',
                "text": 'MHTML (web archive)'
            },
            "Excel": {
                "onclick": 'EXCELOPENXML',
                "text": 'Excel'
            },
            "TIFF": {
                "onclick": 'IMAGE',
                "text": 'TIFF file'
            },
            "Word": {
                "onclick": 'WORDOPENXML',
                "text": 'Word'
            },
            "TXT": {
                "onclick": 'PIPE',
                "text": 'TXT (Pipe delimited)'
            }
        }
        
        logging.info("Starting the report download process.")

        try:
            on_click = format_mapping[report_format]['onclick']
            text = format_mapping[report_format]['text']
            switch_to_latest_window(self.driver)

            self.wait.until(page_loads)
            logging.info("Page load completed.")

            self.wait.until(
                EC.text_to_be_present_in_element_attribute(
                    (By.ID, "ReportViewerControl_AsyncWait"), "style", "visibility: hidden;"
                )
            )
            logging.info("Report viewer is ready.")

            button = self.wait.until(EC.visibility_of_element_located((By.ID, "ReportViewerControl_ctl05_ctl04_ctl00_ButtonImg")))
            button.click()

            xpath = f"//a[contains(@onclick, \"exportReport('{on_click}')\") and contains(text(), '{text}')]"
            csv_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            csv_element.click()
            logging.info("Report download initiated successfully.")

        except Exception as e:
            raise SeleniumException(f"Message : Error occurred during report download.")
        
    def logout(self) -> None:
        """
        Logs out the user by clicking the logout button.

        :returns: None

        :raises SeleniumException: If any issue occurs during logout.
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

def close_other_windows(driver: WebDriver) -> None:
    """
    Closes all browser windows except the main one.

    This function iterates through all open browser windows, closes any 
    additional windows, and switches focus back to the main window.

    :param driver: The Selenium WebDriver instance controlling the browser.
    :type driver: WebDriver
    :returns: None

    :raises SeleniumException: If any issue occurs during closing other windows.
    :raises TimeoutException: If switching to a window or closing it times out.
    """
    logging.info("Attempting to close other browser windows.")
    
    try:
        handles = driver.window_handles[1:]
        if not handles:
            logging.info("No other windows to close.")
        else:
            for handle in handles:
                try:
                    WebDriverWait(driver, 10).until(lambda d: handle in d.window_handles)
                    driver.switch_to.window(handle)
                    logging.info(f"Switched to window: {handle}")

                    time.sleep(1)
                    driver.close()
                    logging.info(f"Closed window: {handle}")

                except TimeoutException:
                    logging.error(f"Timeout while switching to or closing window: {handle}")

        driver.switch_to.window(driver.window_handles[0])
        logging.info("Switched back to the main window.")

    except Exception as e:
        raise SeleniumException(f"Message : Error occurred while closing windows.")
    
def run_logic_for_each_month(from_month: str, to_month: str, logic_function, *args, **kwargs) -> None:
    """
    Iterates through each month between 'from_month' and 'to_month' (inclusive) and executes the provided logic function.

    :param from_month: The starting month in the format "Month YYYY" (e.g., "March 2023").
    :type from_month: str
    :param to_month: The ending month in the format "Month YYYY" (e.g., "February 2024").
    :type to_month: str
    :param logic_function: The function to execute for each month. It should accept:
                           - A string representing the month and year (e.g., "March 2023").
                           - Any additional positional ``*args`` and keyword arguments ``**kwargs``.
    :type logic_function: Callable
    :param args: Additional positional arguments to pass to ``logic_function``.
    :type args: tuple
    :param kwargs: Additional keyword arguments to pass to ``logic_function``.
    :type kwargs: dict
    :returns: None
    :rtype: None

    :raises ValueError: If the date formats are invalid or if ``from_month`` is later than ``to_month``.
    
    :example:
        .. code-block:: python

            def process_month(month_year, flag=None):
                print(f"Processing {month_year}, flag={flag}")

            run_logic_for_each_month("March 2023", "May 2023", process_month, flag="example")
    """
    try:
        start_date = datetime.strptime(from_month, "%B %Y")
        end_date = datetime.strptime(to_month, "%B %Y")
    except ValueError as e:
        raise ValueError("Invalid date format. Expected 'Month YYYY'.")

    if start_date > end_date:
        raise ValueError(f"from_month ('{from_month}') cannot be after to_month ('{to_month}').")

    current_date = start_date

    while current_date <= end_date:
        month_year_str = current_date.strftime("%B %Y")
        logic_function(month_year_str, *args, **kwargs)

        next_month = current_date.month + 1
        next_year = current_date.year
        if next_month > 12:
            next_month = 1
            next_year += 1
        current_date = datetime(next_year, next_month, 1)
    
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from utils.selenium_driver import SeleniumDriver

    BROWSER = 'chrome'
    EXPERITY_URL = 'https://pvpm.practicevelocity.com'
    load_dotenv()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    selenium = SeleniumDriver(browser=BROWSER)
    driver = selenium.setup_driver()
    try:
        experity = ExperityBase(driver)
        experity.open_portal(EXPERITY_URL)
        PORTAL_URL = experity.experity_version()
        experity.login(username, password)
        experity.navigate_to(EXPERITY_URL, PORTAL_URL, "Reports")
        experity.logout()
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        logging.info("Browser closed successfully.")