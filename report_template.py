from math import exp
import os
from re import M
import time
from turtle import down

from dotenv import load_dotenv

# load_dotenv()

# from Others.afc_patient_pdf import DOWNLOAD_DIRECTORY
from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase, close_other_windows
from utils import file_folder
from utils.reports_base import Reports

BROWSER = 'chrome'
TIME_OUT = 300
POLLING_TIME = 2
CLIENT_ID = 3681
EXP_USERNAME ="sjalan@zco02"
PASSWORD ="Graphx@098"
experity_url = 'https://pvpm.practicevelocity.com'


report_export_type = 'CSV'

cnt_27_report_name = 'CNT_27'
cnt_27_from_date = '01/01/2024'
cnt_27_to_date = '12/12/2024'

cnt_19_report_name = 'CNT_19'
cnt_19_from_date = cnt_27_from_date
cnt_19_to_date = cnt_27_to_date

fin_25_report_name = 'FIN_25'
fin_25_from_date = cnt_27_from_date
fin_25_to_date = cnt_27_to_date

adj_11_report_name = 'ADJ_11'
adj_11_from_date = cnt_27_from_date
adj_11_to_date = cnt_27_to_date

fin_18_report_name = 'FIN_18'
fin_18_from_date = cnt_27_from_date
fin_18_to_date = cnt_27_to_date

print(f'Running for Client {CLIENT_ID}')

DOWNLOAD_DIRECTORY = os.path.join(os.getcwd(), 'Temp_Downloads')
print(DOWNLOAD_DIRECTORY)

sel_driver = SeleniumDriver(BROWSER, DOWNLOAD_DIRECTORY)
driver = sel_driver.setup_driver()

experity = ExperityBase(driver, TIME_OUT)

# TODO: Create download directory automatically

if not os.path.exists(DOWNLOAD_DIRECTORY):
    os.makedirs(DOWNLOAD_DIRECTORY)
else:
    # Clear the directory for sanitation
    file_folder.clear_directory_files(DOWNLOAD_DIRECTORY)

# Steps to login
experity.open_portal(experity_url)
experity_version = experity.experity_version()
experity.login(EXP_USERNAME, PASSWORD)

reports = Reports(driver, experity, experity_url, experity_version, report_export_type, DOWNLOAD_DIRECTORY, TIME_OUT)

print(f'Running for report {cnt_27_report_name}')
reports.cnt_27(cnt_27_report_name, cnt_27_from_date, cnt_27_to_date)
print(f'Report {cnt_27_report_name} completed.')

print(f'Running for report {cnt_19_report_name}')
reports.cnt_19(cnt_19_report_name, cnt_19_from_date, cnt_19_to_date)
print(f'Report {cnt_19_report_name} completed.')

print(f'Running for report {fin_25_report_name}')
reports.fin_25(fin_25_report_name, fin_25_from_date, fin_25_to_date)
print(f'Report {fin_25_report_name} completed.')

print(f'Running for report {adj_11_report_name}')
reports.adj_11(adj_11_report_name, adj_11_from_date, adj_11_to_date)
print(f'Report {adj_11_report_name} completed.')

print(f'Running for report {fin_18_report_name}')
reports.fin_18(fin_18_report_name, fin_18_from_date, fin_18_to_date)
print(f'Report {fin_18_report_name} completed.')

time.sleep(1000)
experity.logout()
driver.quit()