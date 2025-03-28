from utils.report_date import get_past_date
from utils.etl.report_config import CURRENT_DATE
from utils.task_queue_adv import TaskQueue
from download_reports import ReportETL

MAX_RETRIES = 3
DATABASE = 'BI_AFC_Experity'

task_q = TaskQueue(MAX_RETRIES)
report = ReportETL(DATABASE, 16)

username = 
password = 

report.experity_login()
