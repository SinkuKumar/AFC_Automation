from math import exp
import os
import time

from dotenv import load_dotenv

# load_dotenv()

# from Others.afc_patient_pdf import DOWNLOAD_DIRECTORY
from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase, close_other_windows
from utils import file_folder

BROWSER = 'chrome'
DOWNLOAD_DIRECTORY = os.path.join(os.getcwd(), 'Temp_Downloads')
print(DOWNLOAD_DIRECTORY)
TIME_OUT = 300
POLLING_TIME = 2
CLIENT_ID = 3681
EXP_USERNAME ="sjalan@zco02"
PASSWORD ="Graphx@098"
experity_url = 'https://pvpm.practicevelocity.com'
report_name = 'CNT_27'
report_export_type = 'CSV'
cnt_27_from_date = '01/01/2024'
cnt_27_to_date = '12/12/2024'
cnt_19_from_date = cnt_27_from_date
cnt_19_to_date = cnt_27_to_date
cnt_19_report_name = 'CNT_19'

sel_driver = SeleniumDriver(BROWSER, DOWNLOAD_DIRECTORY)
driver = sel_driver.setup_driver()

experity = ExperityBase(driver, TIME_OUT)

# TODO: Create download directory automatically

class Reports:
    def __init__(self, driver, experity_url, experity_version, report_export_type, download_directory, time_out):
        self.driver = driver
        self.experity_url = experity_url
        self.experity_version = experity_version
        self.report_export_type = report_export_type
        self.download_directory = download_directory
        self.time_out = time_out
    
    def cnt_27(self, report_name, cnt_27_from_date, cnt_27_to_date):
        experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        experity.search_and_select_report(report_name)
        experity.select_report_date_range(cnt_27_from_date, cnt_27_to_date)
        experity.select_logbook_status(['All'])
        experity.select_financial_class(['All'])
        experity.select_arrival_status(['All'])
        experity.run_report()
        experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory, self.time_out)
        close_other_windows(self.driver)

    def cnt_19(self, report_name, cnt_19_from_date, cnt_19_to_date):
        experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        experity.search_and_select_report(report_name)
        experity.select_report_date_range(cnt_19_from_date, cnt_19_to_date)
        experity.run_report()
        file_folder.wait_for_download(report_name, self.download_directory, self.time_out)
        close_other_windows(self.driver)

# Steps to login
experity.open_portal(experity_url)
experity_version = experity.experity_version()
experity.login(EXP_USERNAME, PASSWORD)

reports = Reports(driver, experity_url, experity_version, report_export_type, DOWNLOAD_DIRECTORY, TIME_OUT)
reports.cnt_27(report_name, cnt_27_from_date, cnt_27_to_date)
reports.cnt_19(cnt_19_report_name, cnt_19_from_date, cnt_19_to_date)

time.sleep(1000)
experity.logout()
driver.quit()

