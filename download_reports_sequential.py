import os
import time

from dotenv import load_dotenv

load_dotenv()

from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase, close_other_windows
from utils import file_folder
from utils.reports_base import Reports
from utils.logging_base import setup_logger
from utils.pyodbc_sql import PyODBCSQL
from utils import transform_csv as t_csv
from utils.sql_queries import CREDENTAILS_QUERY
from utils.task_queue import TaskQueue

TIME_OUT = 900 # 15 minutes
BROWSER = 'chrome'
EXPORT_TYPE = 'CSV'
EXPERITY_URL = "https://pvpm.practicevelocity.com"

sql = PyODBCSQL()
task_q = TaskQueue()

date_stamp = time.strftime("%Y-%m-%d")
time_stamp = time.strftime("%H-%M-%S")
credentials = sql.execute_query(CREDENTAILS_QUERY.format(client_id=3622))
client_id, client_name, username, password = credentials[0]
log_file = os.path.join(os.getcwd(), 'logs', f'Experity_Automation_{client_id}_{date_stamp}.log')

logging = setup_logger(log_file=log_file)
download_directory = os.path.join(os.getcwd(), 'downloads', str(client_id))

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

pay_41_report_name = 'PAY_41'
pay_41_from_date = cnt_27_from_date
pay_41_to_date = cnt_27_to_date

pat_2_report_name = 'PAT_2'
pat_2_from_date = cnt_27_from_date
pat_2_to_date = cnt_27_to_date

lab_01_report_name = 'PAT_2'
lab_01_from_date = cnt_27_from_date
lab_01_to_date = cnt_27_to_date

xry_03_report_name = 'XRY_03'
xry_03_from_date = cnt_27_from_date
xry_03_to_date = cnt_27_to_date

cht_02_report_name = 'XRY_03'
cht_02_from_date = cnt_27_from_date
cht_02_to_date = cnt_27_to_date

med_01_report_name = 'MED_01'
med_01_from_date = cnt_27_from_date
med_01_to_date = cnt_27_to_date

per_02_report_name = 'PER_2'
per_02_from_date = cnt_27_from_date
per_02_to_date = cnt_27_to_date

pat_20_report_name = 'PAT_20'
pat_20_from_date = cnt_27_from_date
pat_20_to_date = cnt_27_to_date

ccr_02_report_name = 'CCR_02'
ccr_02_from_date = cnt_27_from_date
ccr_02_to_date = cnt_27_to_date

ccr_03_report_name = 'CCR_03'
ccr_03_from_date = cnt_27_from_date
ccr_03_to_date = cnt_27_to_date

rev_16_report_name = 'REV_16'
rev_16_date = '2025/01/01' # Give the date properly, in YYYY/MM/DD format.

adj_4_report_name = 'ADJ_4'
adj_4_date = '2025/01/01' # Give the date properly, in YYYY/MM/DD format.

print(f'Running for Client {CLIENT_ID}')

DOWNLOAD_DIRECTORY = os.path.join(os.getcwd(), 'Temp_Downloads')
print(DOWNLOAD_DIRECTORY)

sel_driver = SeleniumDriver(BROWSER, download_directory)
driver = sel_driver.setup_driver()

experity = ExperityBase(driver, TIME_OUT)

if not os.path.exists(download_directory):
    os.makedirs(download_directory)
else:
    file_folder.clear_directory_files(download_directory)

# Steps to login
experity.open_portal(EXPERITY_URL)
experity_version = experity.experity_version()
experity.login(username, password)

reports = Reports(driver, experity, EXPERITY_URL, experity_version, EXPORT_TYPE, download_directory, TIME_OUT)
cnt_27_file_path = reports.cnt_27('CNT_27', '01/01/2022', '03/03/2025')
task_q.add_task(t_csv.cnt_27, cnt_27_file_path, client_id, date_stamp, time_stamp)
# Add task here to upload the data to the database
task_q.add_task(sql.execute_query, "TRUNCATE TABLE CNT_27_Staging_Base")
task_q.add_task(sql.csv_bulk_insert, f"CNT_27_Processed_{time_stamp}.csv", 'CNT_27_Staging_Base')
cnt_19_file_path = reports.cnt_19('CNT_19', '01/01/2022', '03/03/2025')

# TODO: Process the report
# TODO: Insert the data into the database
# TODO: Update the status of the report
reports = Reports(driver, experity, experity_url, experity_version, report_export_type, DOWNLOAD_DIRECTORY, TIME_OUT)

reports.cnt_27(cnt_27_report_name, cnt_27_from_date, cnt_27_to_date)
reports.cnt_19(cnt_19_report_name, cnt_19_from_date, cnt_19_to_date)
reports.fin_25(fin_25_report_name, fin_25_from_date, fin_25_to_date)
reports.adj_11(adj_11_report_name, adj_11_from_date, adj_11_to_date)
reports.fin_18(fin_18_report_name, fin_18_from_date, fin_18_to_date)
reports.pay_41(pay_41_report_name, pay_41_from_date, pay_41_to_date)
reports.pat_2(pat_2_report_name, pat_2_from_date, pat_2_to_date)

reports.lab_01(lab_01_report_name, lab_01_from_date, lab_01_to_date)
reports.xry_03(xry_03_report_name, xry_03_from_date, xry_03_to_date)
reports.cht_02(cht_02_report_name, cht_02_from_date, cht_02_to_date)
reports.med_01(med_01_report_name, med_01_from_date, med_01_to_date)
reports.per_02(per_02_report_name, per_02_from_date, per_02_to_date)
reports.pat_20(pat_20_report_name, pat_20_from_date, pat_20_to_date)

reports.ccr_02(ccr_02_report_name, ccr_02_from_date, ccr_02_to_date)
reports.ccr_03(ccr_03_report_name, ccr_03_from_date, ccr_03_to_date)

reports.rev_16(rev_16_report_name, rev_16_date)
reports.adj_4(adj_4_report_name, adj_4_date)

time.sleep(1000)
experity.logout()
driver.quit()
