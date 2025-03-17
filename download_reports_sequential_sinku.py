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

time.sleep(1000)
experity.logout()
driver.quit()