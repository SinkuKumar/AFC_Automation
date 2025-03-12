"""
Module Description:

- This module contains the script for downloading CNT_19 monthly reports for Experity clients.

:module: CNT_19.py
:platform: Windows, Unix
:synopsis: monthly reports for Experity clients

:date: March 10, 2025

"""

import os
import glob
from datetime import datetime
import logging
# from dotenv import load_dotenv

from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase, close_other_windows
from utils import file_folder as file_operation

def download_report(specific_client: int,
                    user_details: dict,
                    browser: str,
                    cnt_19_from_date: str,
                    cnt_19_to_date: str,
                    logger_instance: logging.getLogger,
                    run_sp: bool = True
                    ):
    """
    Function to complete login and download one particular report.

    :param specific_clients: list of client IDs 
    :type specifi_clients: list

    :param browser: the desired browser to open ['chrome', 'firefox', 'edge']
    :type browser: str

    :param cnt_19_from_date: starting date
    :type cnt_19_from_date: str

    :param cnt_19_to_date: end date
    :param cnt_19_to_date: str

    :param logger_instance: the instance of the logger class
    :type logger_instance: logging.getLogger

    :param run_sp: whether to run stored procedure or not, True or False
    :type run_sp: bool

    Returns None
    """

    today = datetime.now().strftime("%Y_%m_%d")

    download_dir = os.path.join(os.getcwd(), 'Downloaded Reports', today)

    try:
        logger_instance.info("Running report for client_id %s.", specific_client)
        report_name = "CNT_19"

        # for report_name in report_name_list:
        logger_instance.info("Running for report %s.", report_name)

        # Creating a separate download directory for each client
        client_download_dir = os.path.join(download_dir, f"Client {str(specific_client)}")

        # TODO: Remove this in production, create this in top layer.
        if not os.path.exists(client_download_dir):
            os.makedirs(client_download_dir)
        else:
            for file in glob.glob(os.path.join(client_download_dir, f"{report_name}*")):
                os.remove(file)
                logger_instance.info("Previous %s reports in download directory %s cleared.", report_name, client_download_dir)


        # Clearing the download folder ending with today's date
        selenium = SeleniumDriver(browser=browser, download_directory=client_download_dir)
        driver = selenium.setup_driver()
        experity = ExperityBase(driver)

        experity_url = 'https://pvpm.practicevelocity.com'

        experity.open_portal(experity_url)
        logger_instance.info("Opened portal https://pvpm.practicevelocity.com")

        # TODO: Maybe remove this 6 lines in production

        # print(current_client_id)
        username = user_details[specific_client][0]
        password = user_details[specific_client][1]
        # print(username, password)


        # # TODO: Remove this in production, create this in top layer.
        # if not os.path.exists(client_download_dir):
        #     os.makedirs(client_download_dir)
        # # else:
        # #     file_operation.clear_directory_files(client_download_dir)
        # #     logger_instance.info("Client download directory %s already exists, cleared.", client_download_dir)

        experity.login(username, password)

        logger_instance.info("Logged in")

        experity_version = experity.experity_version()
        print("\n")
        logger_instance.info("Got portal URL")


        experity.navigate_to(experity_url, experity_version, "Reports")
        logger_instance.info("Navigate to method called")

        experity.search_and_select_report(report_name)
        logger_instance.info("Search and select report method called")

        # cnt_19_from_date = report_info['report_names'][report_name][0]
        # cnt_19_to_date = report_info['report_names'][report_name][1]

        experity.select_report_date_range(cnt_19_from_date, cnt_19_to_date)
        logger_instance.info("Date report range method called")
        logger_instance.info("Start date: %s, end date: %s.", cnt_19_from_date, cnt_19_to_date)

        # if report_name in ['CNT_19']:
        #     experity.select_logbook_status(['All'])
        #     experity.select_financial_class(['All'])
        #     experity.select_arrival_status(['All'])
        
        # if report_name in ['ADJ_11']:
        #     uncheck_button_identifier_id = "freeunReasonCodescheckall"
        #     check_checkbox_identifier_id = "freeReasonCodescheck2"
        #     experity.uncheck_all_check_all(uncheck_button_identifier_id, check_checkbox_identifier_id)

        # Uncheck all check all option ??
        experity.run_report()
        logger_instance.info("Run report method called")

        experity.download_report('CSV')
        logger_instance.info("Download report method called")

        file_operation.wait_for_download(report_name, client_download_dir)
        logger_instance.info("Downloaded report %s.", report_name)

        # Close the window and switch to the main window
        close_other_windows(driver)
        logger_instance.info("Closed other windows")

        logger_instance.info("Report %s completed.", report_name)
        print("\n")

        if run_sp:
            logger_instance.info("Running stored procedure for report %s.", report_name)
            logger_instance.info("...........................")
            logger_instance.info("...........................")
            logger_instance.info("...........................")

        # Logout
        experity.logout()
        logger_instance.info("Logged out")
        driver.quit()

    except Exception as e:
        logger_instance.info("Error occurred: %s %s", type(e).__name__, e)
        print("Error occurred: %s %s", type(e).__name__, e)


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

    # today = datetime.now().strftime("%Y_%m_%d")
    # report_details ={}

    start_date = "01/01/2025"
    end_date = datetime.now().strftime("%m/%d/%Y")
    """
    The structure of report_details and user details are present in the
    `reportDetailsAndUserDetailsStructures.js` file.
    # report_details['report_names'] = {
    #     "CNT_19" : [start_date, end_date],
    #     "ADJ_11" : [start_date, end_date],
    #     'CNT_19' : [start_date, end_date],
    #     "PAY_41" : [start_date, end_date],
    #     "PAT_2" : [start_date, end_date],
    #     "CNT_19" : [start_date, end_date]
    #     }
    # report_details['download_dir'] = os.path.join(os.getcwd(), 'Downloaded Reports', today)

    # Put the name of the required clients here.
    specific_clients = [3681, 3671, 16]

    browser_name = "chrome"
    """
    User details is a dictionary.
    The keys of user details are the client_ids.
    The values are lists:
        1. the first element is username for the client
        2. the second element is password for the client
    """

    logger_inst = get_logger_name("mtd_reports")

    download_report(specific_client = specific_clients,
                    browser = browser_name,
                    cnt_19_from_date = start_date,
                    cnt_19_to_date = end_date,
                    logger_instance=logger_inst,
                    run_sp=False
                    )
'''