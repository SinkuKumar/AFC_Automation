import os
import sys
from pdb import run
import time
from datetime import datetime
import logging
import traceback
from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase
from utils.file_folder import FileOperations

def complete_report(report_info: dict,
                    user_info: dict,
                    browser: str,
                    cnt_27_from_date: str,
                    cnt_27_to_date: str
                    ):
    """
    Function to complete login and download one particular report.

    :param report_info: dictionary, containing the details of the report.
        ```
        report_info = {'download_dir' : '', 'report_name' : ''}
        ```
    :type report_info: dict

    :param user_info: dictionary containing the username and password
        ```
            user_info = {'username' : '', 'password' : ''}
        ```
    :type user_info: dict

    :logger_instance: the instance of the logger class
    :type logger_instance: logging.getLogger

    :param browser: the desired browser to open ['chrome', 'firefox', 'edge']
    :type browser: str

    Returns None
    """
    try:
        download_dir = report_info['download_dir']
        report_name = report_info['report_name']

        # TODO: Remove this in production, create this in top layer.
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        experity_url = 'https://pvpm.practicevelocity.com'

        selenium = SeleniumDriver(browser=browser, download_directory=download_dir)
        driver = selenium.setup_driver()
        experity = ExperityBase(driver)
        file_operation = FileOperations()

        experity.open_portal(experity_url)
        # logger_instance.info("Opened portal")

        # TODO: Maybe remove this 6 lines in production
        username = user_info["username"]
        password = user_info['password']

        experity.login(username, password)
        # logger_instance.info("Logged in")

        experity_version = experity.get_portal_url()
        # logger_instance.info("Got portal URL")

        experity.navigate_to(experity_url, experity_version, "Reports")
        # logger_instance.info("Navigate to method called")

        experity.search_and_select_report("CNT_27")
        # logger_instance.info("Search and select report method called")

        experity.select_report_date_range(cnt_27_from_date, cnt_27_to_date)
        # logger_instance.info("Date report range method called")

        experity.select_logbook_status(['All'])

        experity.select_financial_class(['All'])
        experity.select_arrival_status(['All'])

        # Uncheck all check all option ??
        experity.run_report()
        # logger_instance.info("Run report method called")
        experity.download_report('CSV')
        file_operation.wait_for_download(report_name, download_dir)
        # logger_instance.info("Download report method called")

    except Exception as e:
        # logger_instance.info("Error occurred: %s %s", type(e).__name__, e)
        print("Error occurred: %s %s", type(e).__name__, e)

'''
def get_logger_name(log_name):
    """
    Method to define the logger for this module.

    :param log_name: name of the logger

    :returns: A logger instance
    :rtype: logger.getLogger()
    """
    logger = logging.getLogger(log_name)
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
    return logger
'''
'''
if __name__ == "__main__":
    load_dotenv('.env')

    today = datetime.now().strftime("%Y_%m_%d")
    report_info ={}
    report_info['report_name'] = "CNT_27"
    report_info['download_dir'] = os.path.join(os.getcwd(), 'Downloaded Reports', today)
    browser = "chrome"

    user_info = {}
    user_info['client_id'] = os.getenv("CLIENT_ID")
    user_info["username"] = os.getenv('EXP_USERNAME')
    user_info["password"] = os.getenv('PASSWORD')

    logger_inst = get_logger_name("main")

    complete_report(report_info = report_info,
                    browser = browser, user_info=user_info,
                    logger_instance=logger_inst
                    )

'''