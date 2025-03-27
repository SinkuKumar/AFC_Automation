import os
import sys

from dotenv import load_dotenv

load_dotenv()

from utils import file_folder
from utils.task_queue import TaskQueue
from utils.pyodbc_sql import PyODBCSQL
from utils.logging_base import setup_logger
from utils.experity_base import ExperityBasex
from utils.selenium_driver import SeleniumDriver

from utils.etl.transform_csv import TransformCSV
from utils.etl.extract_report import ExtractReports
from utils.etl.load_sql import BulkLoadSQL
from utils.etl import report_config


class ReportETL:
    def __init__(self, db_name, client_id):
        self.client_id = client_id
        self.BROWSER = report_config.BROWSER
        self.LOG_DIR = report_config.LOG_DIR
        self.TIME_OUT = report_config.TIME_OUT
        self.TIME_STAMP = report_config.TIME_STAMP
        self.DATE_STAMP = report_config.DATE_STAMP
        self.EXRTY_URL = report_config.EXPERITY_URL
        self.EXPORT_TYPE = report_config.EXPORT_TYPE
        self.CRED_Q = report_config.CREDENTIALS_QUERY
        self.DT_STAMP = report_config.DATE_TIME_STAMP
        self.LOG_STAMP = report_config.LOG_DT_STAMP
        self.DWLD_DIR = os.path.join(report_config.DWLD_DIR, str(self.client_id))
        file_folder.init_directory(self.DWLD_DIR)
        self.sql = PyODBCSQL(db_name)
        sel_driver = SeleniumDriver(self.BROWSER, self.DWLD_DIR)
        self.driver = sel_driver.setup_driver()
        self.experity = ExperityBase(self.driver, self.TIME_OUT)
        self.task_q = TaskQueue()
        self.trns_csv = TransformCSV(self.client_id, self.DT_STAMP)
        self.load_csv = BulkLoadSQL(self.sql, empty_table=True)
        self.rpt_config = report_config.ReportConfig(self.client_id)

        file_folder.create_directories([self.LOG_DIR, self.DWLD_DIR])
        self.CLIENT_TODAY_DIR = os.path.join(self.DWLD_DIR, self.DATE_STAMP)
        file_folder.create_directories([self.CLIENT_TODAY_DIR])

    def experity_login(self):
        # NOTE: It'll take only the first client credentials
        client_id, username, password = self.sql.get_users_credentials([self.client_id])[0]
        self.experity.open_portal(self.EXRTY_URL)
        self.experity_version = self.experity.experity_version()
        self.exct_rep = ExtractReports(self.driver, self.experity, self.EXRTY_URL, self.experity_version, self.EXPORT_TYPE, self.DWLD_DIR, self.TIME_OUT)
        self.experity.login(username, password)

    def etl_cnt_27(self, from_date, to_date):
        cnt_27_cfg = self.rpt_config.cnt_27(from_date, to_date)
        self.exct_rep.cnt_27(cnt_27_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(cnt_27_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.cnt_27, os.path.join(self.DWLD_DIR, cnt_27_cfg['file_name']), os.path.join(self.DWLD_DIR, cnt_27_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, cnt_27_cfg['processed_file']), cnt_27_cfg['base_table'], cnt_27_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, cnt_27_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_cnt_19(self, from_date, to_date):
        cnt_19_cfg = self.rpt_config.cnt_19(from_date, to_date)
        self.exct_rep.cnt_19(cnt_19_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(cnt_19_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.cnt_19, os.path.join(self.DWLD_DIR, cnt_19_cfg['file_name']), os.path.join(self.DWLD_DIR,cnt_19_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report,os.path.join(self.DWLD_DIR, cnt_19_cfg['processed_file']), cnt_19_cfg['base_table'], cnt_19_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, cnt_19_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_adj_11(self, from_date, to_date):
        adj_11_cfg = self.rpt_config.adj_11(from_date, to_date)
        self.exct_rep.adj_11(adj_11_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(adj_11_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.adj_11, os.path.join(self.DWLD_DIR, adj_11_cfg['file_name']), os.path.join(self.DWLD_DIR, adj_11_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, adj_11_cfg['processed_file']), adj_11_cfg['base_table'], adj_11_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, adj_11_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_fin_18(self, from_date, to_date):
        fin_18_cfg = self.rpt_config.fin_18(from_date, to_date)
        self.exct_rep.fin_18(fin_18_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(fin_18_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.fin_18, os.path.join(self.DWLD_DIR, fin_18_cfg['file_name']), os.path.join(self.DWLD_DIR, fin_18_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, fin_18_cfg['processed_file']), fin_18_cfg['base_table'], fin_18_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, fin_18_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_pay_41(self, from_date, to_date):
        pay_41_cfg = self.rpt_config.pay_41(from_date, to_date)
        self.exct_rep.pay_41(pay_41_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(pay_41_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.pay_41, os.path.join(self.DWLD_DIR, pay_41_cfg['file_name']), os.path.join(self.DWLD_DIR, pay_41_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, pay_41_cfg['processed_file']), pay_41_cfg['base_table'], pay_41_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, pay_41_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_xry_03(self, from_date, to_date):
        xry_03_cfg = self.rpt_config.xry_03(from_date, to_date)
        self.exct_rep.xry_03(xry_03_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(xry_03_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.xry_03, os.path.join(self.DWLD_DIR, xry_03_cfg['file_name']), os.path.join(self.DWLD_DIR, xry_03_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report,  os.path.join(self.DWLD_DIR, xry_03_cfg['processed_file']), xry_03_cfg['base_table'], xry_03_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, xry_03_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def rtl_pay_10(self, from_date, to_date):
        pay_10_cfg = self.rpt_config.pay_10(from_date, to_date)
        self.exct_rep.pay_10(pay_10_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(pay_10_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.pay_10, os.path.join(self.DWLD_DIR, pay_10_cfg['file_name']), os.path.join(self.DWLD_DIR, pay_10_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, pay_10_cfg['processed_file']), pay_10_cfg['base_table'], pay_10_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, pay_10_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_ccr_02(self, from_date, to_date):
        ccr2_cfg = self.rpt_config.ccr_2(from_date, to_date)
        self.exct_rep.ccr_02(ccr2_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(ccr2_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.ccr_02, os.path.join(self.DWLD_DIR, ccr2_cfg['file_name']), os.path.join(self.DWLD_DIR, ccr2_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, ccr2_cfg['file_name']), ccr2_cfg['base_table'], ccr2_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, ccr2_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_ccr_03(self, from_date, to_date):
        ccr3_cfg = self.rpt_config.ccr_3(from_date, to_date)
        self.exct_rep.ccr_03(ccr3_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(ccr3_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.ccr_03, os.path.join(self.DWLD_DIR, ccr3_cfg['file_name']), os.path.join(self.DWLD_DIR, ccr3_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, ccr3_cfg['processed_file']), ccr3_cfg['base_table'], ccr3_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, ccr3_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_per_02(self, from_date, to_date):
        per_02_cfg = self.rpt_config.per_2(from_date, to_date)
        self.exct_rep.per_02(per_02_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(per_02_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.per_02, os.path.join(self.DWLD_DIR, per_02_cfg['file_name']), os.path.join(self.DWLD_DIR, per_02_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, per_02_cfg['processed_file']), per_02_cfg['base_table'], per_02_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, per_02_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_med_01(self, from_date, to_date):
        med_1_cfg = self.rpt_config.med_01(from_date, to_date)
        self.exct_rep.med_01(med_1_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(med_1_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.med_01, os.path.join(self.DWLD_DIR, med_1_cfg['file_name']), os.path.join(self.DWLD_DIR, med_1_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, med_1_cfg['processed_file']), med_1_cfg['base_table'], med_1_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, med_1_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_pat_20(self, from_date, to_date):
        pat_20_cfg = self.rpt_config.pat_20(from_date, to_date)
        self.exct_rep.pat_20(pat_20_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(pat_20_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.pat_20, os.path.join(self.DWLD_DIR, pat_20_cfg['file_name']), os.path.join(self.DWLD_DIR, pat_20_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, pat_20_cfg['processed_file']), pat_20_cfg['base_table'], pat_20_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, pat_20_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_lab_01(self, from_date, to_date):
        lab_1_cfg = self.rpt_config.lab_01(from_date, to_date)
        self.exct_rep.lab_01(lab_1_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(lab_1_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.lab_01, os.path.join(self.DWLD_DIR, lab_1_cfg['file_name']), os.path.join(self.DWLD_DIR, lab_1_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, lab_1_cfg['processed_file']), lab_1_cfg['base_table'], lab_1_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, lab_1_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_cht_02(self, from_date, to_date):
        cht_2_cfg = self.rpt_config.cht_02(from_date, to_date)
        self.exct_rep.cht_02(cht_2_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(cht_2_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.cht_02, os.path.join(self.DWLD_DIR, cht_2_cfg['file_name']), os.path.join(self.DWLD_DIR, cht_2_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, cht_2_cfg['processed_file']), cht_2_cfg['base_table'], cht_2_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, cht_2_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_pat_02(self, from_date, to_date):
        pat_2_cfg = self.rpt_config.pat_2(from_date, to_date)
        self.exct_rep.pat_2(pat_2_cfg['report_name'], from_date, to_date)
        table_columns = self.load_csv.get_column_names(pat_2_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.pat_02, os.path.join(self.DWLD_DIR, pat_2_cfg['file_name']), os.path.join(self.DWLD_DIR, pat_2_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, pat_2_cfg['processed_file']), pat_2_cfg['base_table'], pat_2_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, pat_2_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_adj_04(self, from_month, to_month):
        adj_4_cfg = self.rpt_config.adj_4(from_month, to_month)
        self.exct_rep.adj_4(adj_4_cfg['report_name'], from_month, to_month)
        self.task_q.add_task(self.trns_csv.combine_csv_files, self.DWLD_DIR, os.path.join(self.DWLD_DIR, adj_4_cfg['file_name']), adj_4_cfg['report_name'])
        table_columns = self.load_csv.get_column_names(adj_4_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.adj_4, os.path.join(self.DWLD_DIR, adj_4_cfg['file_name']), os.path.join(self.DWLD_DIR, adj_4_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, adj_4_cfg['processed_file']), adj_4_cfg['base_table'], adj_4_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, adj_4_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_pay_04(self, from_month, to_month):
        pay_4_cfg = self.rpt_config.pay_4(from_month, to_month)
        self.exct_rep.pay_4(pay_4_cfg['report_name'], from_month, to_month)
        self.task_q.add_task(self.trns_csv.combine_csv_files, self.DWLD_DIR, os.path.join(self.DWLD_DIR, pay_4_cfg['file_name']), pay_4_cfg['report_name'])
        table_columns = self.load_csv.get_column_names(pay_4_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.pay_4, os.path.join(self.DWLD_DIR, pay_4_cfg['file_name']), os.path.join(self.DWLD_DIR, pay_4_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, pay_4_cfg['processed_file']), pay_4_cfg['base_table'], pay_4_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, pay_4_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def etl_rev_16(self, from_date, to_date):
        rev_16_cfg = self.rpt_config.rev_16(from_date, to_date)
        self.exct_rep.rev_16(rev_16_cfg['report_name'], from_date, to_date)
        self.task_q.add_task(self.trns_csv.combine_csv_files, self.DWLD_DIR, os.path.join(self.DWLD_DIR, rev_16_cfg['file_name']), rev_16_cfg['report_name'])
        table_columns = self.load_csv.get_column_names(rev_16_cfg['base_table'])
        self.task_q.add_task(self.trns_csv.rev_16, os.path.join(self.DWLD_DIR, rev_16_cfg['file_name']), os.path.join(self.DWLD_DIR, rev_16_cfg['processed_file']), table_columns)
        self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, rev_16_cfg['processed_file']), rev_16_cfg['base_table'], rev_16_cfg['staging_table'])
        self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, rev_16_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    def experity_logout(self):
        self.experity.logout()
        self.driver.quit()
        self.task_q.wait_for_completion()

    # def etl_fin_25(self, from_date, to_date):
    #     fin_25_cfg = self.rpt_config.fin_25(from_date, to_date)
    #     self.exct_rep.fin_25(fin_25_cfg['report_name'], from_date, to_date)
    #     table_columns = self.load_csv.get_column_names(fin_25_cfg['base_table'])
    #     self.task_q.add_task(self.trns_csv.fin_25, os.path.join(self.DWLD_DIR, fin_25_cfg['file_name']), os.path.join(self.DWLD_DIR, fin_25_cfg['processed_file']), table_columns)
    #     self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, fin_25_cfg['processed_file']), fin_25_cfg['base_table'], fin_25_cfg['staging_table'])
    #     self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, fin_25_cfg['processed_file']), self.CLIENT_TODAY_DIR)

    # def etl_rev_19(self, from_month, to_month):
    #     rev_19_cfg = self.rpt_config.rev_19(from_month, to_month)
    #     self.exct_rep.rev_19(rev_19_cfg['report_name'], from_month, to_month)
    #     self.task_q.add_task(self.trns_csv.combine_csv_files, self.DWLD_DIR, os.path.join(self.DWLD_DIR, rev_19_cfg['file_name']), rev_19_cfg['report_name'])
    #     table_columns = self.load_csv.get_column_names(rev_19_cfg['base_table'])
    #     self.task_q.add_task(self.trns_csv.rev_19, os.path.join(self.DWLD_DIR, rev_19_cfg['file_name']), os.path.join(self.DWLD_DIR, rev_19_cfg['processed_file']), table_columns)
    #     self.task_q.add_task(self.load_csv.load_report, os.path.join(self.DWLD_DIR, rev_19_cfg['processed_file']), rev_19_cfg['base_table'], rev_19_cfg['staging_table'])
    #     self.task_q.add_task(file_folder.move_file, os.path.join(self.DWLD_DIR, rev_19_cfg['processed_file']), self.CLIENT_TODAY_DIR)

def execute_report_functions(client_id, mode, function_list, function_args=None):
    all_report_function_names = ["etl_cnt_27", "etl_cnt_19", "etl_adj_11", "etl_fin_18", "etl_pay_41", "etl_xry_03", "rtl_pay_10", "etl_ccr_02", "etl_ccr_03", "etl_per_02", "etl_med_01", "etl_pat_20", "etl_lab_01", "etl_cht_02", "etl_pat_02", "etl_rev_16", "etl_pay_04", "etl_adj_04"]
    
    function_list = [name.lower() for name in function_list]

    if function_args is None:
        function_args = {}

    function_name_map = {func.split("_", 1)[-1]: func for func in all_report_function_names}

    normalized_args = {key.lower(): value for key, value in function_args.items()}

    etl_reports = ReportETL('BI_AFC_Experity', client_id)
    etl_reports.experity_login()

    def execute_func(short_name):
        full_func_name = function_name_map.get(short_name)
        if full_func_name:
            args = normalized_args.get(short_name, {})
            method = getattr(etl_reports, full_func_name, None)
            if callable(method):
                try:
                    method(**args)
                except TypeError as e:
                    print(f"Error calling {full_func_name}: {e}")
            else:
                print(f"Warning: {full_func_name} is not a valid method.")

    if mode == "include":
        for short_name in function_list:
            execute_func(short_name)

    elif mode == "exclude":
        for short_name in function_name_map.keys():
            if short_name not in function_list:
                execute_func(short_name)

    elif mode == "all":
        for short_name in function_name_map.keys():
            execute_func(short_name)
    else:
        print("Invalid Mode")

    etl_reports.experity_logout()
    etl_reports.task_q.wait_for_completion()
