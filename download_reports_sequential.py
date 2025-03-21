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
LOG_STAMP = report_config.LOG_DT_STAMP

sql = PyODBCSQL('analytics_db')
task_q = TaskQueue()

file_folder.create_directories([LOG_DIR, DWLD_DIR])

# credentials = sql.execute_query(CRED_Q.format(client_id=3671))
# client_id, client_name, username, password = credentials[0]
client_id, client_name, username, password = [3671, 'Test', 'sjalan@zma04', 'Graphx@987']

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
load_csv = BulkLoadSQL(sql, empty_table=True)
rpt_config = report_config.ReportConfig(client_id)
cnt_27_cfg = rpt_config.cnt_27()
cnt_19_cfg = rpt_config.cnt_19()
adj_11_cfg = rpt_config.adj_11()
fin_18_cfg = rpt_config.fin_18()
pay_41_cfg = rpt_config.pay_41()
pat_2_cfg = rpt_config.pat_2()
lab_1_cfg = rpt_config.lab_01()
xry_03_cfg = rpt_config.xry_03()
cht_2_cfg = rpt_config.cht_02()
med_1_cfg = rpt_config.med_01()
per_02_cfg = rpt_config.per_2()
pat_20_cfg = rpt_config.pat_20()
ccr2_cfg = rpt_config.ccr_2()
ccr3_cfg = rpt_config.ccr_3()
rev_16_cfg = rpt_config.rev_16()
pay_4_cfg = rpt_config.pay_4()
adj_4_cfg = rpt_config.adj_4() #
pay_10_cfg = rpt_config.pay_10()
fin_25_cfg = rpt_config.fin_25()
rev_19_cfg = rpt_config.rev_19()

CLIENT_TODAY_DIR = os.path.join(DWLD_DIR, DATE_STAMP)
file_folder.create_directories([CLIENT_TODAY_DIR])

# Extract, Transform, Load CNT_27
exct_rep.cnt_27(cnt_27_cfg['report_name'], cnt_27_cfg['from_date'], cnt_27_cfg['to_date'])
task_q.add_task(trns_csv.cnt_27, os.path.join(DWLD_DIR, cnt_27_cfg['file_name']), os.path.join(DWLD_DIR, cnt_27_cfg['processed_file']))
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, cnt_27_cfg['processed_file']), cnt_27_cfg['base_table'], cnt_27_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, cnt_27_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load CNT_19
exct_rep.cnt_19(cnt_19_cfg['report_name'], cnt_19_cfg['from_date'], cnt_19_cfg['to_date'])
task_q.add_task(trns_csv.cnt_19, os.path.join(DWLD_DIR, cnt_19_cfg['file_name']), os.path.join(DWLD_DIR,cnt_19_cfg['processed_file']))
task_q.add_task(load_csv.load_report,os.path.join(DWLD_DIR, cnt_19_cfg['processed_file']), cnt_19_cfg['base_table'], cnt_19_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, cnt_19_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load ADJ_11
exct_rep.adj_11(adj_11_cfg['report_name'], adj_11_cfg['from_date'], adj_11_cfg['to_date'])
task_q.add_task(trns_csv.adj_11, os.path.join(DWLD_DIR, adj_11_cfg['file_name']), os.path.join(DWLD_DIR, adj_11_cfg['processed_file']))
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, adj_11_cfg['processed_file']), adj_11_cfg['base_table'], adj_11_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, adj_11_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load FIN_18
exct_rep.fin_18(fin_18_cfg['report_name'], fin_18_cfg['from_date'], fin_18_cfg['to_date'])
task_q.add_task(trns_csv.fin_18, os.path.join(DWLD_DIR, fin_18_cfg['file_name']), os.path.join(DWLD_DIR, fin_18_cfg['processed_file']))
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, fin_18_cfg['processed_file']), fin_18_cfg['base_table'], fin_18_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, fin_18_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load PAY_41
exct_rep.pay_41(pay_41_cfg['report_name'], pay_41_cfg['from_date'], pay_41_cfg['to_date'])
task_q.add_task(trns_csv.pay_41, os.path.join(DWLD_DIR, pay_41_cfg['file_name']), os.path.join(DWLD_DIR, pay_41_cfg['processed_file']))
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, pay_41_cfg['processed_file']), pay_41_cfg['base_table'], pay_41_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, pay_41_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load XRY_03
exct_rep.xry_03(xry_03_cfg['report_name'], xry_03_cfg['from_date'], xry_03_cfg['to_date'])
task_q.add_task(trns_csv.xry_03, os.path.join(DWLD_DIR, xry_03_cfg['file_name']), os.path.join(DWLD_DIR, xry_03_cfg['processed_file']))
task_q.add_task(load_csv.load_report,  os.path.join(DWLD_DIR, xry_03_cfg['processed_file']), xry_03_cfg['base_table'], xry_03_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, xry_03_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load PAY_10
exct_rep.pay_10(pay_10_cfg['report_name'], pay_10_cfg['from_date'], pay_10_cfg['to_date'])
table_columns = load_csv.get_column_names(pay_10_cfg['base_table'])
task_q.add_task(trns_csv.pay_10, os.path.join(DWLD_DIR, pay_10_cfg['file_name']), os.path.join(DWLD_DIR, pay_10_cfg['processed_file']), table_columns)
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, pay_10_cfg['processed_file']), pay_10_cfg['base_table'], pay_10_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, pay_10_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load FIN_25
exct_rep.fin_25(fin_25_cfg['report_name'], fin_25_cfg['from_date'], fin_25_cfg['to_date'])
table_columns = load_csv.get_column_names(fin_25_cfg['base_table'])
task_q.add_task(trns_csv.fin_25, os.path.join(DWLD_DIR, fin_25_cfg['file_name']), os.path.join(DWLD_DIR, fin_25_cfg['processed_file']), table_columns)
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, fin_25_cfg['processed_file']), fin_25_cfg['base_table'], fin_25_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, fin_25_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load CCR_2
exct_rep.ccr_02(ccr2_cfg['report_name'], ccr2_cfg['from_date'], ccr2_cfg['to_date'])
task_q.add_task(trns_csv.ccr_02, os.path.join(DWLD_DIR, ccr2_cfg['file_name']), os.path.join(DWLD_DIR, ccr2_cfg['processed_file']))
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, ccr2_cfg['file_name']), ccr2_cfg['base_table'], ccr2_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, ccr2_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load CCR_3
exct_rep.ccr_03(ccr3_cfg['report_name'], ccr3_cfg['from_date'], ccr3_cfg['to_date'])
task_q.add_task(trns_csv.ccr_03, os.path.join(DWLD_DIR, ccr3_cfg['file_name']), os.path.join(DWLD_DIR, ccr3_cfg['processed_file']))
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, ccr3_cfg['processed_file']), ccr3_cfg['base_table'], ccr3_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, ccr3_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load REV_19
exct_rep.rev_19(rev_19_cfg['report_name'], rev_19_cfg['from_month'], rev_19_cfg['to_month'])
task_q.add_task(trns_csv.combine_csv_files, DWLD_DIR, os.path.join(DWLD_DIR, rev_19_cfg['file_name']), rev_19_cfg['report_name'])
table_columns = load_csv.get_column_names(rev_19_cfg['base_table'])
task_q.add_task(trns_csv.rev_19, os.path.join(DWLD_DIR, rev_19_cfg['file_name']), os.path.join(DWLD_DIR, rev_19_cfg['processed_file']), table_columns)
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, rev_19_cfg['processed_file']), rev_19_cfg['base_table'], rev_19_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, rev_19_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load PER_02
exct_rep.per_02(per_02_cfg['report_name'], per_02_cfg['from_date'], per_02_cfg['to_date'])
task_q.add_task(trns_csv.per_02, os.path.join(DWLD_DIR, per_02_cfg['file_name']), os.path.join(DWLD_DIR, per_02_cfg['processed_file']))
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, per_02_cfg['processed_file']), per_02_cfg['base_table'], per_02_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, per_02_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load MED_01
exct_rep.med_01(med_1_cfg['report_name'], med_1_cfg['from_date'], med_1_cfg['to_date'])
task_q.add_task(trns_csv.med_01, os.path.join(DWLD_DIR, med_1_cfg['file_name']), os.path.join(DWLD_DIR, med_1_cfg['processed_file']))
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, med_1_cfg['processed_file']), med_1_cfg['base_table'], med_1_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, med_1_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load PAT_20
exct_rep.pat_20(pat_20_cfg['report_name'], pat_20_cfg['from_date'], pat_20_cfg['to_date'])
task_q.add_task(trns_csv.pat_20, os.path.join(DWLD_DIR, pat_20_cfg['file_name']), os.path.join(DWLD_DIR, pat_20_cfg['processed_file']))
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, pat_20_cfg['processed_file']), pat_20_cfg['base_table'], pat_20_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, pat_20_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load LAB_01
exct_rep.lab_01(lab_1_cfg['report_name'], lab_1_cfg['from_date'], lab_1_cfg['to_date'])
task_q.add_task(trns_csv.lab_01, os.path.join(DWLD_DIR, lab_1_cfg['file_name']), os.path.join(DWLD_DIR, lab_1_cfg['processed_file']))
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, lab_1_cfg['processed_file']), lab_1_cfg['base_table'], lab_1_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, lab_1_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load CHT_02
exct_rep.cht_02(cht_2_cfg['report_name'], cht_2_cfg['from_date'], cht_2_cfg['to_date'])
task_q.add_task(trns_csv.cht_02, os.path.join(DWLD_DIR, cht_2_cfg['file_name']), os.path.join(DWLD_DIR, cht_2_cfg['processed_file']))
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, cht_2_cfg['processed_file']), cht_2_cfg['base_table'], cht_2_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, cht_2_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load PAT_02
exct_rep.pat_2(pat_2_cfg['report_name'], pat_2_cfg['from_date'], pat_2_cfg['to_date'])
task_q.add_task(trns_csv.pat_02, os.path.join(DWLD_DIR, pat_2_cfg['file_name']), os.path.join(DWLD_DIR, pat_2_cfg['processed_file']))
task_q.add_task(load_csv.load_report, os.path.join(DWLD_DIR, pat_2_cfg['processed_file']), pat_2_cfg['base_table'], pat_2_cfg['staging_table'])
task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, pat_2_cfg['processed_file']), CLIENT_TODAY_DIR)

experity.logout()
driver.quit()