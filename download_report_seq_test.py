import os
import time

from dotenv import load_dotenv

load_dotenv()

from utils import file_folder
from utils.task_queue import TaskQueue
from utils.pyodbc_sql import PyODBCSQL
# from utils.logging_base import setup_logger
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

sql = PyODBCSQL('analytics_db')
task_q = TaskQueue()

file_folder.create_directories([LOG_DIR, DWLD_DIR])

# credentials = sql.execute_query(CRED_Q.format(client_id=3671))
# client_id, client_name, username, password = credentials[0]
client_id, client_name, username, password = [1001, 'Test', 'sjalan@zma04', 'Graphx@987']

# log_file = os.path.join(LOG_DIR, f'Experity_Automation_{client_id}_{DT_STAMP}.log')

# logging = setup_logger(log_file=log_file)
DWLD_DIR = os.path.join(DWLD_DIR, str(client_id))
CLIENT_TODAY_DIR = os.path.join(DWLD_DIR, DATE_STAMP)
TEMP_DWLD_DIR = os.path.join(DWLD_DIR, f"TEMP_{DATE_STAMP}_{TIME_STAMP.replace(':', '-')}")


sel_driver = SeleniumDriver(BROWSER, TEMP_DWLD_DIR)
driver = sel_driver.setup_driver()
experity = ExperityBase(driver, TIME_OUT)

# file_folder.init_directory(DWLD_DIR)

# Login to experity
experity.open_portal(EXRTY_URL)
experity_version = experity.experity_version()
experity.login(username, password)

task_q = TaskQueue()
exct_rep = ExtractReports(driver, experity, EXRTY_URL, experity_version, EXPORT_TYPE, TEMP_DWLD_DIR, TIME_OUT)
trns_csv = TransformCSV(client_id, DT_STAMP)
load_csv = BulkLoadSQL(sql, empty_table=True)
rpt_config = report_config.ReportConfig(client_id)
pay_10_cfg = rpt_config.pay_10()
rev_19_cfg = rpt_config.rev_19()
fin_25_cfg = rpt_config.fin_25()

file_folder.create_directories([CLIENT_TODAY_DIR, TEMP_DWLD_DIR])

# Extract, Transform, Load PAY_10 - DONE
# exct_rep.pay_10(pay_10_cfg['report_name'], pay_10_cfg['from_date'], pay_10_cfg['to_date'])
# table_columns = load_csv.get_column_names(pay_10_cfg['base_table'])
# task_q.add_task(trns_csv.pay_10, os.path.join(TEMP_DWLD_DIR, pay_10_cfg['file_name']), os.path.join(CLIENT_TODAY_DIR, pay_10_cfg['processed_file']), table_columns)
# task_q.add_task(load_csv.load_report, os.path.join(CLIENT_TODAY_DIR, pay_10_cfg['processed_file']), pay_10_cfg['base_table'], pay_10_cfg['staging_table'])
# task_q.add_task(file_folder.delete_directories, TEMP_DWLD_DIR)

# # Extract, Transform, Load REV_19 - Check Again (deletion of directory creating issue)
# exct_rep.rev_19(rev_19_cfg['report_name'], rev_19_cfg['from_month'], rev_19_cfg['to_month'])
# task_q.add_task(trns_csv.combine_csv_files, TEMP_DWLD_DIR, os.path.join(TEMP_DWLD_DIR, rev_19_cfg['file_name']), rev_19_cfg['report_name'])
# table_columns = load_csv.get_column_names(rev_19_cfg['base_table'])
# task_q.add_task(trns_csv.rev_19, os.path.join(TEMP_DWLD_DIR, rev_19_cfg['file_name']), os.path.join(CLIENT_TODAY_DIR, rev_19_cfg['processed_file']), table_columns)
# task_q.add_task(file_folder.delete_directories, TEMP_DWLD_DIR)

# # Extract, Transform, Load FIN_25 - DONE
# exct_rep.fin_25(fin_25_cfg['report_name'], fin_25_cfg['from_date'], fin_25_cfg['to_date'])
# table_columns = load_csv.get_column_names(fin_25_cfg['base_table'])
# task_q.add_task(trns_csv.fin_25, os.path.join(TEMP_DWLD_DIR, fin_25_cfg['file_name']), os.path.join(CLIENT_TODAY_DIR, fin_25_cfg['processed_file']), table_columns)
# task_q.add_task(load_csv.load_report, os.path.join(CLIENT_TODAY_DIR, fin_25_cfg['processed_file']), fin_25_cfg['base_table'], fin_25_cfg['staging_table'])
# task_q.add_task(file_folder.delete_directories, TEMP_DWLD_DIR)

experity.logout()
driver.quit()
