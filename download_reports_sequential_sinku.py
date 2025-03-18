import os
import time

from dotenv import load_dotenv

load_dotenv()

from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase
from utils import file_folder
from utils.reports_base import Reports
from utils.logging_base import setup_logger
from utils.pyodbc_sql import PyODBCSQL
from utils import transform_csv as t_csv
from utils.sql_queries import CREDENTAILS_QUERY
from utils.task_queue import TaskQueue, insert_data

TIME_OUT = 900 # 15 minutes
BROWSER = 'chrome'
EXPORT_TYPE = 'CSV'
EXPERITY_URL = "https://pvpm.practicevelocity.com"

sql = PyODBCSQL('BI_AFC_Experity')
task_q = TaskQueue()

file_folder.create_directories(['logs'])

date_stamp = time.strftime("%Y-%m-%d")
time_stamp = time.strftime("%H-%M-%S")
credentials = sql.execute_query(CREDENTAILS_QUERY.format(client_id=3622))
client_id, client_name, username, password = credentials[0]
log_file = os.path.join(os.getcwd(), 'logs', f'Experity_Automation_{client_id}_{date_stamp}.log')

logging = setup_logger(log_file=log_file)
download_directory = os.path.join(os.getcwd(), 'downloads', str(client_id))

sel_driver = SeleniumDriver(BROWSER, download_directory)
driver = sel_driver.setup_driver()

experity = ExperityBase(driver, TIME_OUT)

file_folder.init_directory(download_directory)

# Steps to login
experity.open_portal(EXPERITY_URL)
experity_version = experity.experity_version()
experity.login(username, password)

reports = Reports(driver, experity, EXPERITY_URL, experity_version, EXPORT_TYPE, download_directory, TIME_OUT)
cnt_27_staging_table = f"CNT_27_Staging_{client_id}"
processed_file_path = os.path.join(download_directory, f"CNT_27_Processed_{time_stamp}.csv")
cnt_27_raw_file_path = reports.cnt_27('CNT_27', '01/01/2022', '03/03/2025')
insert_data(task_q, sql, cnt_27_staging_table, processed_file_path, t_csv.cnt_27, cnt_27_raw_file_path, client_id, date_stamp, time_stamp)
"""
task_q.add_task(t_csv.cnt_27, cnt_27_file_path, client_id, date_stamp, time_stamp)
try:
    sql.execute_query(f"SELECT TOP 0 * INTO {cnt_27_staging_table} FROM CNT_27_Staging_Base;")
except Exception as e:
    pass
task_q.add_task(sql.truncate_table, cnt_27_staging_table)
task_q.add_task(sql.csv_bulk_insert, processed_file_path, cnt_27_staging_table)"
"""

time.sleep(1000)
experity.logout()
driver.quit()