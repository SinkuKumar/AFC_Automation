import os
from datetime import datetime
import logging
from dotenv import load_dotenv

from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase, close_other_windows
from utils.file_folder import FileOperations

def complete_report(report_info: dict,
                    user_info: dict,
                    browser: str,
                    from_date: str,
                    to_date: str,
                    logger_instance: logging.getLogger,
                    run_sp: bool = True
                    ):
    """
    Function to complete login and download one particular report.

    :param report_info: dictionary, containing the details of the report.
        ```
        {
            'report_names' : {
                "report_1" : [start_date, end_date], 
                "report_2" : [start_date, end_date],
                'report_3' : [start_date, end_date],
                "report_4" : [start_date, end_date]
                },
            'download_dir' : 'download directory'
        }
        ```
    :type report_info: dict

    :param user_info: dictionary containing the username and password
        ```
            user_info = {'username' : '', 'password' : ''}
        ```
    :type user_info: dict

    :param browser: the desired browser to open ['chrome', 'firefox', 'edge']
    :type browser: str

    :param from_date: starting date
    :type from_date: str

    :param to_date: end date
    :param to_date: str

    :param logger_instance: the instance of the logger class
    :type logger_instance: logging.getLogger

    :param run_sp: whether to run stored procedure or not, True or False
    :type run_sp: bool

    Returns None
    """
    try:
        download_dir = report_info['download_dir']
        report_name_list = report_info['report_names'].keys()

        selenium = SeleniumDriver(browser=browser, download_directory=download_dir)
        driver = selenium.setup_driver()
        experity = ExperityBase(driver)
        file_operation = FileOperations()
        
        # TODO: Remove this in production, create this in top layer.
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        file_operation.clear_directory_files(download_dir)
        logger_instance.info("Download directory %s cleared.", download_dir)

        experity_url = 'https://pvpm.practicevelocity.com'

        experity.open_portal(experity_url)
        logger_instance.info("Opened portal")

        # TODO: Maybe remove this 6 lines in production
        client_ids = user_info.keys()

        for current_client_id in client_ids:
            print(current_client_id)
            username = user_info[current_client_id][0]
            password = user_info[current_client_id][1]
            print(username, password)

            experity.login(username, password)
            exit()
            logger_instance.info("Logged in")

            experity_version = experity.get_portal_url()
            logger_instance.info("Got portal URL")

            for report_name in report_name_list:

                logger_instance.info("Running for report %s.", report_name)

                experity.navigate_to(experity_url, experity_version, "Reports")
                logger_instance.info("Navigate to method called")

                experity.search_and_select_report(report_name)
                logger_instance.info("Search and select report method called")

                from_date = report_info['report_names'][report_name][0]
                to_date = report_info['report_names'][report_name][1]

                experity.select_report_date_range(from_date, to_date)
                logger_instance.info("Date report range method called")
                logger_instance.info("Start date: %s, end date: %s.", from_date, to_date)

                if report_name in ['CNT_27']:
                    experity.select_logbook_status(['All'])
                    experity.select_financial_class(['All'])
                    experity.select_arrival_status(['All'])
                
                if report_name in ['ADJ_11']:
                    uncheck_button_identifier_id = "freeunReasonCodescheckall"
                    check_checkbox_identifier_id = "freeReasonCodescheck2"
                    experity.uncheck_all_check_all(uncheck_button_identifier_id, check_checkbox_identifier_id)

                # Uncheck all check all option ??
                experity.run_report()
                logger_instance.info("Run report method called")

                experity.download_report('CSV')
                logger_instance.info("Download report method called")

                file_operation.wait_for_download(report_name, download_dir)
                logger_instance.info("Downloaded report %s.", report_name)

                # Close the window and switch to the main window
                close_other_windows(driver)
                logger_instance.info("Closed other windows")

                logger_instance.info("Report %s completed.", report_name)

                if run_sp:
                    logger_instance.info("Running stored procedure for report %s.", report_name)

            # Logout
            experity.logout()
            logger_instance.info("Logged out")

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

if __name__ == "__main__":
    load_dotenv('utils/.env')

    today = datetime.now().strftime("%Y_%m_%d")
    report_details ={}

    start_date = "01/01/2025"
    end_date = datetime.now().strftime("%m/%d/%Y")
    '''
    Report_details has the following structure:
    
    '''
    report_details['report_names'] = {
        "CNT_27" : [start_date, end_date], 
        "ADJ_11" : [start_date, end_date],
        'FIN_18' : [start_date, end_date],
        "PAY_41" : [start_date, end_date],
        "PAT_2" : [start_date, end_date],
        "CNT_19" : [start_date, end_date]
        }
    report_details['download_dir'] = os.path.join(os.getcwd(), 'Downloaded Reports', today)

    browser_name = "chrome"
    '''
    User details is a dictionary.
    The keys of user details are the client_ids.
    The values are lists:
        1. the first element is username for the client
        2. the second element is password for the client
    '''
    user_details = {}
    client_id = os.getenv("CLIENT_ID")
    user_details[client_id] = [os.getenv('EXP_USERNAME'), os.getenv('PASSWORD')]
    # print(user_details)

    logger_inst = get_logger_name("mtd_reports")

    complete_report(report_info = report_details,
                    user_info = user_details,
                    browser = browser_name,
                    from_date = start_date,
                    to_date = end_date,
                    logger_instance=logger_inst,
                    run_sp=False
                    )
