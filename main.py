import os
import time
import logging
import traceback
from dotenv import load_dotenv
from utils.file_folder import FileOperations
from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase, close_other_windows

BROWSER = 'chrome'
DOWNLOAD_DIR = os.getcwd()
WINDOW_WIDTH = None
WINDOW_HEIGHT = None
EXPERITY_URL = 'https://pvpm.practicevelocity.com'
PORTAL_URL = '25_1'

current_dir = os.getcwd()
download_dir = os.path.join(os.path.dirname(current_dir), 'AFC_Test_Files')

selenium = SeleniumDriver(browser=BROWSER, download_directory=download_dir, window_width=WINDOW_WIDTH, window_height= WINDOW_HEIGHT)
driver = selenium.setup_driver()

load_dotenv()
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

try:
    experity = ExperityBase(driver)
    file_operation = FileOperations()

    experity.open_portal(EXPERITY_URL)
    experity.login(username, password)
    experity.navigate_to_sub_nav(EXPERITY_URL, PORTAL_URL, "Reports")
    experity.select_pm_report('Financials', 'Revenue', 'REV 14')
    experity.select_pm_report_filter('REV 14', cls_month_end="December 2024", rev_code="Surgery")
    # experity.select_pm_report('Financials', 'Adjustments', 'ADJ 0')
    # experity.select_pm_report_filter('ADJ 0', 'December 2024', 'November 2024')
    # time.sleep(5)
    # experity.run_report()
    # file_operation.clear_directory_files(download_dir)
    # experity.download_report('Excel')
    # file_operation.wait_for_download('ADJ_0', download_dir)
    # close_other_windows(driver)
    # experity.navigate_to_recievables_page(12345)
    # experity.search_and_select_report('CNT 27')
    # experity.select_report_date_range('12/01/2024', '12/30/2024')
    # experity.select_logbook_status(['All'])
    # experity.select_financial_class(['All'])
    # experity.select_arrival_status(['All'])
    # experity.run_report()
    # file_operation.clear_directory_files(download_dir)
    # experity.download_report('CSV')
    # file_operation.wait_for_download('CNT_27', download_dir)
    # close_other_windows(driver)
    time.sleep(5)
    experity.logout()

except Exception as e:
    logging.error("An unexpected error occured : \n" + traceback.format_exc())
    print(e)
finally:
    driver.quit()
    logging.info("Browser closed successfully.")