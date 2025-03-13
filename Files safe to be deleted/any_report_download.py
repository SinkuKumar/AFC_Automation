import os
from datetime import datetime, timedelta
from venv import logger
from dotenv import load_dotenv
import logging

from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase, close_other_windows
from utils.file_folder import FileOperations

def complete_report(staging_table_name: str,
                    report_info: dict,
                    user_info: dict,
                    browser: str,
                    from_date: str,
                    to_date: str,
                    logger_instance: logging.getLogger,
                    uncheck_all_check_all: list = ['All'],
                    run_sp: bool = True,
                    ):
    """
    Function to complete login and download one particular report.

    :param staging_table_name: name of the staging table
    :type staging_table_name: str

    :param report_info: dictionary contains the details of the report.
    ```
    >>> print(report_info = {'download_dir' : '', 'report_name' : ''})
    ```
    :type report_info: dict

    :param user_info: dictionary contains the username and password
     ```
    user_info = {'username' : '', 'password' : ''}
    ```
    :type user_info: dict

    :param browser: the desired browser to open ['chrome', 'firefox', 'edge']
    :type browser: str

    :param from_date: starting date
    :type from_date: str

    :param to_date: end date
    :type to_date: end date

    :param uncheck_all_check_all: checkboxes to check or uncheck, default ['All']
    :type uncheck_all_check_all: list

    :param run_sp: stored procedure will run if True, else will not run.
        By default, True
    :type run_sp: bool

    Returns None
    """
    try:
        logger_instance.info("Running %s report.", report_info['report_name'])
        download_dir = report_info['download_dir']
        report_name = report_info['report_name']

        # TODO: Remove this in production, create this in top layer.
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            logger_instance.info("Created download path %s",download_dir)
        else:
            logger_instance.info("Download path already exists.")

        experity_url = 'https://pvpm.practicevelocity.com'

        selenium = SeleniumDriver(browser=browser, download_directory=download_dir)
        driver = selenium.setup_driver()
        experity = ExperityBase(driver)
        file_operation = FileOperations()

        experity.open_portal(experity_url)
        logger_instance.info("Opened portal")

        # TODO: Maybe remove this 6 lines in production
        username = user_info["username"]
        password = user_info['password']

        experity.login(username, password)
        logger_instance.info("Logged in")

        experity_version = experity.experity_version()
        print(experity_version)

        logger_instance.info("Got portal URL")

        experity.navigate_to(experity_url, experity_version, "Reports")
        logger_instance.info("Navigate to method called")

        experity.search_and_select_report(report_name)
        logger_instance.info("Search and select report method called")

        experity.select_report_date_range(from_date, to_date)
        logger_instance.info("Date report range method called")

        experity.select_logbook_status(uncheck_all_check_all)
        experity.select_financial_class(uncheck_all_check_all)
        experity.select_arrival_status(uncheck_all_check_all)

        # Uncheck all check all option ??
        experity.run_report()
        logger_instance.info("Run report method called")
        experity.download_report('CSV')
        file_operation.wait_for_download(report_name, download_dir)
        logger_instance.info("Download report method called")


        # Close other windows
        close_other_windows(driver)
        logger_instance.info("Closed other windows")
        
        # Logout
        experity.logout()
        logger_instance.info("Logged out")

        if run_sp:
            # run stored procedure
            # print(f'Running stored procedure for {report_name} repot from staging table.')
            # print(f'Staging table name: {staging_table_name}')
            logger_instance.info("Running stored procedure for %s from staging table %s", report_name, staging_table_name)

    except Exception as e:
        logger_instance.info("Error occurred: %s %s", type(e).__name__, e)
        # print("Error occurred: %s %s",
        # type(e).__name__, e)


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

    current_date = datetime.now()
    CNT_19_days_back = 60
    from_date = current_date - timedelta(days=CNT_19_days_back)
    from_date = from_date.replace(day=1)
    CNT_19_from_date = from_date.strftime("%m/%d/%Y")
    CNT_19_to_date = current_date.strftime("%m/%d/%Y")
    CNT_19_staging_table = 'CNT_19_Temp_MTD'

    complete_report(report_info = report_info,
                    browser = browser, 
                    user_info=user_info,
                    from_date = CNT_19_from_date,
                    to_date=CNT_19_to_date,
                    run_sp=False
                    )
'''