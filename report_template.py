from math import exp
import os
import time

from dotenv import load_dotenv

# load_dotenv()

# from Others.afc_patient_pdf import DOWNLOAD_DIRECTORY
from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase, close_other_windows
from utils import file_folder
from utils.reports import Reports

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
fin_25_from_date = cnt_27_from_date
fin_25_to_date = cnt_27_to_date
fin_25_report_name = 'FIN_25'

sel_driver = SeleniumDriver(BROWSER, DOWNLOAD_DIRECTORY)
driver = sel_driver.setup_driver()

experity = ExperityBase(driver, TIME_OUT)

# TODO: Create download directory automatically

# Clear the directory for sanitation
file_folder.clear_directory_files(DOWNLOAD_DIRECTORY)

# Steps to login
experity.open_portal(experity_url)
experity_version = experity.experity_version()
experity.login(EXP_USERNAME, PASSWORD)

reports = Reports(driver, experity, experity_url, experity_version, report_export_type, DOWNLOAD_DIRECTORY, TIME_OUT)
reports.cnt_27(report_name, cnt_27_from_date, cnt_27_to_date)
reports.cnt_19(cnt_19_report_name, cnt_19_from_date, cnt_19_to_date)
reports.fin_25(fin_25_report_name, fin_25_from_date, fin_25_to_date)
time.sleep(1000)
experity.logout()
driver.quit()

