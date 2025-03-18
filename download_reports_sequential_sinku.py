import os
import time

from dotenv import load_dotenv

load_dotenv()

from utils import file_folder
from utils.task_queue import TaskQueue
from utils.pyodbc_sql import PyODBCSQL
from utils.logging_base import setup_logger
from utils.experity_base import ExperityBase
from utils.selenium_driver import SeleniumDriver

from utils.etl.transform_csv import TransformCSV
from utils.etl.extract_report import ExtractReports
from utils.etl.load_sql import BulkLoadSQL
from utils.etl import report_config

BROWSER = report_config.BROWSER
LOG_DIR = report_config.LOG_DIR
TIME_OUT = report_config.TIME_OUT
DWLD_DIR = report_config.DWLD_DIR
TIME_STAMP = report_config.TIME_STAMP
DATE_STAMP = report_config.DATE_STAMP
EXRTY_URL = report_config.EXPERITY_URL
EXPORT_TYPE = report_config.EXPORT_TYPE
CRED_Q = report_config.CREDENTIALS_QUERY
DT_STAMP = report_config.DATE_TIME_STAMP

sql = PyODBCSQL('BI_AFC_Experity')
task_q = TaskQueue()

file_folder.create_directories([LOG_DIR, DWLD_DIR])

credentials = sql.execute_query(CRED_Q.format(client_id=3671))
client_id, client_name, username, password = credentials[0]

log_file = os.path.join(LOG_DIR, f'Experity_Automation_{client_id}_{DT_STAMP}.log')

logging = setup_logger(log_file=log_file)
DWLD_DIR = os.path.join(DWLD_DIR, str(client_id))

sel_driver = SeleniumDriver(BROWSER, DWLD_DIR)
driver = sel_driver.setup_driver()
experity = ExperityBase(driver, TIME_OUT)

file_folder.init_directory(DWLD_DIR)

# Login to experity
experity.open_portal(EXRTY_URL)
experity_version = experity.experity_version()
experity.login(username, password)


task_q = TaskQueue()
exct_rep = ExtractReports(driver, experity, EXRTY_URL, experity_version, EXPORT_TYPE, DWLD_DIR, TIME_OUT)
trns_csv = TransformCSV(client_id, DT_STAMP)
load_csv = BulkLoadSQL(sql, empty_table=True)
rpt_config = report_config.ReportConfig(client_id)
cnt_27_cfg = rpt_config.cnt_27()
cnt_19_cfg = rpt_config.cnt_19()
CLIENT_TODAY_DIR = os.path.join(DWLD_DIR, DATE_STAMP)
file_folder.create_directories([CLIENT_TODAY_DIR])

# Extract, Transform, Load CNT_27
exct_rep.cnt_27(cnt_27_cfg['report_name'], cnt_27_cfg['from_date'], cnt_27_cfg['to_date'])
task_q.add_task(trns_csv.cnt_27, os.path.join(DWLD_DIR, cnt_27_cfg['file_name']), os.path.join(DWLD_DIR, cnt_27_cfg['processed_file']))
# task_q.add_task(load_csv.load_report, cnt_27_cfg['processed_file'], cnt_27_cfg['base_table'], cnt_27_cfg['staging_table'])

# Extract, Transform, Load CNT_19
exct_rep.cnt_19(cnt_19_cfg['report_name'], cnt_19_cfg['from_date'], cnt_19_cfg['to_date'])
# task_q.add_task(trns_csv.cnt_19, cnt_19_cfg['file_name'], cnt_19_cfg['processed_file'])
# task_q.add_task(load_csv.load_report, cnt_19_cfg['processed_file'], cnt_19_cfg['base_table'], cnt_19_cfg['staging_table'])

# Move all the file to the date folder
file_folder.move_files_only(DWLD_DIR, CLIENT_TODAY_DIR)
experity.logout()
driver.quit()