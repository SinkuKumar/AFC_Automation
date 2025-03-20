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
cnt_27_cfg = rpt_config.cnt_27() # DONE
cnt_19_cfg = rpt_config.cnt_19() # DONE
adj_11_cfg = rpt_config.adj_11() # DONE
fin_18_cfg = rpt_config.fin_18() # DONE
pay_41_cfg = rpt_config.pay_41()
pat_2_cfg = rpt_config.pat_2()
lab_1_cfg = rpt_config.lab_01()
xry_3_cfg = rpt_config.xry_03()
cht_2_cfg = rpt_config.cht_02()
med_1_cfg = rpt_config.med_01()
per_2_cfg = rpt_config.per_2()
pat_20_cfg = rpt_config.pat_20()
ccr2_cfg = rpt_config.ccr_2()
ccr3_cfg = rpt_config.ccr_3()
rev_16_cfg = rpt_config.rev_16()
pay_4_cfg = rpt_config.pay_4()
adj_4_cfg = rpt_config.adj_4()

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
# task_q.add_task(trns_csv.pay_41, os.path.join(DWLD_DIR, pay_41_cfg['file_name']), os.path.join(DWLD_DIR, pay_41_cfg['processed_file']))
# task_q.add_task(load_csv.load_report, pay_41_cfg['processed_file'], pay_41_cfg['base_table'], pay_41_cfg['staging_table'])
# task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, pay_41_cfg['processed_file']), CLIENT_TODAY_DIR)

"""
# Extract, Transform, Load PAT_2
exct_rep.pat_2(pat_2_cfg['report_name'], pat_2_cfg['from_date'], pat_2_cfg['to_date'])
# task_q.add_task(trns_csv.pat_2, os.path.join(DWLD_DIR, pat_2_cfg['file_name']), os.path.join(DWLD_DIR, pat_2_cfg['processed_file']))
# task_q.add_task(load_csv.load_report, pat_2_cfg['processed_file'], pat_2_cfg['base_table'], pat_2_cfg['staging_table'])
# task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, pat_2_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load LAB_1
exct_rep.lab_01(lab_1_cfg['report_name'], lab_1_cfg['from_date'], lab_1_cfg['to_date'])
# task_q.add_task(trns_csv.lab_1, os.path.join(DWLD_DIR, lab_1_cfg['file_name']), os.path.join(DWLD_DIR, lab_1_cfg['processed_file']))
# task_q.add_task(load_csv.load_report, lab_1_cfg['processed_file'], lab_1_cfg['base_table'], lab_1_cfg['staging_table'])
# task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, lab_1_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load XRY_3
exct_rep.xry_03(xry_3_cfg['report_name'], xry_3_cfg['from_date'], xry_3_cfg['to_date'])
# task_q.add_task(trns_csv.xry_3, os.path.join(DWLD_DIR, xry_3_cfg['file_name']), os.path.join(DWLD_DIR, xry_3_cfg['processed_file']))
# task_q.add_task(load_csv.load_report, xry_3_cfg['processed_file'], xry_3_cfg['base_table'], xry_3_cfg['staging_table'])
# task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, xry_3_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load CHT_2
exct_rep.cht_02(cht_2_cfg['report_name'], cht_2_cfg['from_date'], cht_2_cfg['to_date'])
# task_q.add_task(trns_csv.cht_2, os.path.join(DWLD_DIR, cht_2_cfg['file_name']), os.path.join(DWLD_DIR, cht_2_cfg['processed_file']))
# task_q.add_task(load_csv.load_report, cht_2_cfg['processed_file'], cht_2_cfg['base_table'], cht_2_cfg['staging_table'])
# task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, cht_2_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load MED_1
exct_rep.med_01(med_1_cfg['report_name'], med_1_cfg['from_date'], med_1_cfg['to_date'])
# task_q.add_task(trns_csv.med_1, os.path.join(DWLD_DIR, med_1_cfg['file_name']), os.path.join(DWLD_DIR, med_1_cfg['processed_file']))
# task_q.add_task(load_csv.load_report, med_1_cfg['processed_file'], med_1_cfg['base_table'], med_1_cfg['staging_table'])
# task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, med_1_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load PER_2
exct_rep.per_02(per_2_cfg['report_name'], per_2_cfg['from_date'], per_2_cfg['to_date'])
# task_q.add_task(trns_csv.per_2, os.path.join(DWLD_DIR, per_2_cfg['file_name']), os.path.join(DWLD_DIR, per_2_cfg['processed_file']))
# task_q.add_task(load_csv.load_report, per_2_cfg['processed_file'], per_2_cfg['base_table'], per_2_cfg['staging_table'])
# task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, per_2_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load PAT_20
exct_rep.pat_20(pat_20_cfg['report_name'], pat_20_cfg['from_date'], pat_20_cfg['to_date'])
# task_q.add_task(trns_csv.pat_20, os.path.join(DWLD_DIR, pat_20_cfg['file_name']), os.path.join(DWLD_DIR, pat_20_cfg['processed_file']))
# task_q.add_task(load_csv.load_report, pat_20_cfg['processed_file'], pat_20_cfg['base_table'], pat_20_cfg['staging_table'])
# task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, pat_20_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load CCR_2
exct_rep.ccr_02(ccr2_cfg['report_name'], ccr2_cfg['from_date'], ccr2_cfg['to_date'])
# task_q.add_task(trns_csv.ccr_2, os.path.join(DWLD_DIR, ccr2_cfg['file_name']), os.path.join(DWLD_DIR, ccr2_cfg['processed_file']))
# task_q.add_task(load_csv.load_report, ccr2_cfg['processed_file'], ccr2_cfg['base_table'], ccr2_cfg['staging_table'])
# task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, ccr2_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load CCR_3
exct_rep.ccr_03(ccr3_cfg['report_name'], ccr3_cfg['from_date'], ccr3_cfg['to_date'])
# task_q.add_task(trns_csv.ccr_3, os.path.join(DWLD_DIR, ccr3_cfg['file_name']), os.path.join(DWLD_DIR, ccr3_cfg['processed_file']))
# task_q.add_task(load_csv.load_report, ccr3_cfg['processed_file'], ccr3_cfg['base_table'], ccr3_cfg['staging_table'])
# task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, ccr3_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load REV_16
exct_rep.rev_16(rev_16_cfg['report_name'], rev_16_cfg['from_date'], rev_16_cfg['to_date'])
# task_q.add_task(trns_csv.rev_16, os.path.join(DWLD_DIR, rev_16_cfg['file_name']), os.path.join(DWLD_DIR, rev_16_cfg['processed_file']))
# task_q.add_task(load_csv.load_report, rev_16_cfg['processed_file'], rev_16_cfg['base_table'], rev_16_cfg['staging_table'])
# task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, rev_16_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load PAY_4
exct_rep.pay_4(pay_4_cfg['report_name'], pay_4_cfg['from_date'], pay_4_cfg['to_date'])
# task_q.add_task(trns_csv.pay_4, os.path.join(DWLD_DIR, pay_4_cfg['file_name']), os.path.join(DWLD_DIR, pay_4_cfg['processed_file']))
# task_q.add_task(load_csv.load_report, pay_4_cfg['processed_file'], pay_4_cfg['base_table'], pay_4_cfg['staging_table'])
# task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, pay_4_cfg['processed_file']), CLIENT_TODAY_DIR)

# Extract, Transform, Load ADJ_4
exct_rep.adj_4(adj_4_cfg['report_name'], adj_4_cfg['from_date'], adj_4_cfg['to_date'])
# task_q.add_task(trns_csv.adj_4, os.path.join(DWLD_DIR, adj_4_cfg['file_name']), os.path.join(DWLD_DIR, adj_4_cfg['processed_file']))
# task_q.add_task(load_csv.load_report, adj_4_cfg['processed_file'], adj_4_cfg['base_table'], adj_4_cfg['staging_table'])
# task_q.add_task(file_folder.move_file, os.path.join(DWLD_DIR, adj_4_cfg['file_name']), CLIENT_TODAY_DIR)
"""

experity.logout()
driver.quit()