import os
import threading
import logging

from dotenv import load_dotenv

from utils.file_folder import FileOperations
from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase, close_other_windows, switch_to_latest_window

load_dotenv(".env")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logs

# Configure logging to ignore TensorFlow warnings
logging.getLogger("tensorflow").setLevel(logging.ERROR)


BROSWER = 'chrome'
DOWNLOAD_PATH = '/Downloads'
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
TIMEOUT = 100

USERNAME = os.getenv('EXP_USERNAME')
PASSWORD = os.getenv('PASSWORD')

EXPERITY_URL = os.getenv("EXPERITY_URL")
PORTAL_URL = os.getenv("PORTAL_URL")

reports = {
    "mtd_reports" : ['CNT_27']
    # "mtd_reports" : ['CNT_27', 'CNT_19', 'FIN_18', 'ADJ_11', 'PAY_41', 'PAT_2'],
    # "mtd_mb_reports" : ['CNT_27', 'CNT_19', 'FIN_18', 'ADJ_11', 'PAY_41', 'PAT_2'],
    # "other_reports" :  ['LAB_01', 'XRY_03', 'CHT_02', 'MED_01', 'PAT_20', 'PER_2'],
    # "ccr_reports" : ['CCR_02', 'CCR_03']
}

# client_list = [[640,655,822,3650,3657,3696,3698,3724,3716,3705],
#                [3622,3625,3630,3649,3678,3705,3665,3720,3725,3726],
#                [36,489,3624,3670,3672,3697,3718,3735,3736]
#                ]
# mb_clients = [3681, 3671, 16]

sel_driver = SeleniumDriver(BROSWER, DOWNLOAD_PATH, WINDOW_WIDTH, WINDOW_HEIGHT)
driver = sel_driver.setup_driver()

experity = ExperityBase(driver, TIMEOUT)
file_operation = FileOperations()


def download_reports(report_name: str, experity_instance: ExperityBase, experity_url: str,
                     experity_username: str, experity_password: str, portal_url: str):
    """
    Performs download operations for each report.

    Args:
    :param report_name: Name of the report
    :type report_name: str

    :param experity_instance: Object of Experity class
    :type experity_instance: ExperityBase

    :param experity_url: https URL of the experity portal
    :type experity_url: str


    """
    try:
        experity_instance.open_portal(experity_url)
        experity_instance.login(experity_username, experity_password)
        experity_instance.select_sub_navigation_item(experity_url, PORTAL_URL, "Reports")
        experity_instance.search_and_select_report(report_name=report_name)
        experity_instance.run_report()
        experity_instance.download_report("CSV")
        switch_to_latest_window(driver = driver)
        close_other_windows(driver = driver)
    except Exception as e:
        print(f'Error occurred: {e}')
        experity_instance.logout()

for report_class, report_list in reports.items():
    print(f"Report class {report_class}: ")
    for i in report_list:
        download_reports(i,experity_instance=experity)
    print('\n')
