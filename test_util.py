import os
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
LOG_STAMP = report_config.LOG_DT_STAMP

# sql = PyODBCSQL('analytics_db')
task_q = TaskQueue()

file_folder.create_directories([LOG_DIR, DWLD_DIR])

# credentials = sql.execute_query(CRED_Q.format(client_id=3671))
# client_id, client_name, username, password = credentials[0]
client_id, client_name, username, password = [3698, 'AFC-Mandeep', 'sjalan@zca10', 'Graphx@222']

log_file = os.path.join(LOG_DIR, f'Experity_Automation_{client_id}_{LOG_STAMP}.log')

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
# load_csv = BulkLoadSQL(sql, empty_table=True)
rpt_config = report_config.ReportConfig(client_id)

CLIENT_TODAY_DIR = os.path.join(DWLD_DIR, DATE_STAMP)
file_folder.create_directories([CLIENT_TODAY_DIR])

def pre_execution():
    print("=== Starting Execution ===")

def post_execution():
    experity.logout()
    driver.quit()

def pay_10_report(from_date: str = None, to_date: str = None, from_month: str = None, to_month : str = None):
    pay_10_cfg = rpt_config.pay_10()
    pay_10_from_date, pay_10_to_date = from_date or pay_10_cfg['from_date'], to_date or pay_10_cfg['to_date']
    exct_rep.pay_10(pay_10_cfg['report_name'], pay_10_from_date, pay_10_to_date)
    task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, pay_10_cfg['file_name']), CLIENT_TODAY_DIR)

def rev_19_report(from_date: str = None, to_date: str = None, from_month: str = None, to_month : str = None):
    rev_19_cfg = rpt_config.rev_19()
    rev_19_from_month, rev_19_to_month = from_month or rev_19_cfg['from_month'], to_month or rev_19_cfg['to_month']
    exct_rep.rev_19(rev_19_cfg['report_name'], rev_19_from_month, rev_19_to_month)
    task_q.add_task(trns_csv.combine_csv_files, DWLD_DIR, os.path.join(DWLD_DIR, rev_19_cfg['file_name']), rev_19_cfg['report_name'])
    task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, rev_19_cfg['file_name']), CLIENT_TODAY_DIR)

def fin_25_report(from_date: str = None, to_date: str = None, from_month: str = None, to_month : str = None):
    fin_25_cfg = rpt_config.fin_25()
    fin_25_from_month, fin_25_to_month = from_date or fin_25_cfg['from_date'], to_date or fin_25_cfg['to_date']
    exct_rep.fin_25(fin_25_cfg['report_name'], fin_25_from_month, fin_25_to_month)
    task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, fin_25_cfg['file_name']), CLIENT_TODAY_DIR)

def execute_functions(mode, function_list, from_date = None, to_date  = None, from_month: str = None, to_month : str = None):
    all_report_function_names = ["pay_10_report", "rev_19_report", "fin_25_report"]

    function_list = [name.lower() for name in function_list]

    pre_execution()

    if mode == "include":
        for func in all_report_function_names:
            if any(func.startswith(name) for name in function_list):
                globals()[func](from_date, to_date, from_month, to_month)

    elif mode == "exclude":
        for func in all_report_function_names:
            if not any(func.startswith(name) for name in function_list):
                globals()[func](from_date, to_date, from_month, to_month)

    elif mode == "all":
        for func in all_report_function_names:
            globals()[func](from_date, to_date, from_month, to_month)
    else:
        print("Invalid Mode")

    post_execution()

    task_q.wait_for_completion()


###############################################


def execute_functions(mode, function_list, from_date = None, to_date  = None, from_month: str = None, to_month : str = None):
    all_report_function_names = ["Sample_ABC", "Sample_EFG", "Sample_IJK"]

    function_list = [name.lower() for name in function_list]

    pre_execution()

    if mode == "include":
        for func in all_report_function_names:
            if any(func.endswith(name) for name in function_list):
                globals()[func](from_date, to_date, from_month, to_month)

    elif mode == "exclude":
        for func in all_report_function_names:
            if not any(func.endswith(name) for name in function_list):
                globals()[func](from_date, to_date, from_month, to_month)

    elif mode == "all":
        for func in all_report_function_names:
            globals()[func](from_date, to_date, from_month, to_month)
    else:
        print("Invalid Mode")

    post_execution()

    task_q.wait_for_completion()