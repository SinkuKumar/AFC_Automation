import os
import time
import logging
import traceback
from dotenv import load_dotenv
from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase
from utils.file_folder import FileOperations

def complete_report(report_name: str, download_dir: str, browser: str, username: str):
    '''
    Function to complete login and download one particular report.

    Args:
    :param report_name: Name of the report to be downloaded
    :type report_name: str

    :param download_dir: directory where the file needs to be downloaded
    :type download_dir: str

    :param browser: the desired browser to open ['chrome', 'firefox', 'edge']
    :type browser: str

    :param username: the login username of the client
    :type username Str
    '''
    try:
        # TODO: Remove this in production, create this in top layer.
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        experity_url = 'https://pvpm.practicevelocity.com'

        selenium = SeleniumDriver(browser=browser, download_directory=download_dir)
        driver = selenium.setup_driver()
        experity = ExperityBase(driver)
        file_operation = FileOperations()

        load_dotenv()

        logger = logging.getLogger("my_logger")
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        log_format = f"{{asctime}} : {__name__} : {{levelname}} : {{message}}"
        console_formatter = logging.Formatter(
            fmt = log_format,
            style = "{"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        username = os.getenv('EXP_USERNAME')
        password = os.getenv('PASSWORD')

        experity.open_portal(experity_url)
        logger.info("Opened portal")

        experity.login(username, password)
        logger.info("Logged in")

        experity_version = experity.get_portal_url()
        logger.info("Got portal URL")

        experity.navigate_to(experity_url, experity_version, "Reports")
        logger.info("Navigate to method called")

        experity.search_and_select_report("CNT_27")
        logger.info("Search and select report method called")

        experity.select_report_date_range('02/02/2025', '02/02/2025')
        logger.info("Date report range method called")

        experity.select_logbook_status(['All'])

        experity.select_financial_class(['All'])
        experity.select_arrival_status(['All'])

        # Uncheck all check all option ??
        experity.run_report()
        logger.info("Run report method called")
        experity.download_report('CSV')
        file_operation.wait_for_download(report_name, download_dir)
        logger.info("Download report method called")

        # Implement the stored procedure partx
        

    except Exception as e:
        logger.info("Error occurred: %s %s", type(e).__name__, e)



report_name = "CNT_27"
download_dir = os.path.join(os.getcwd(), 'Downloaded Reports')