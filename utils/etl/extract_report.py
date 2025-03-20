import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils.experity_base import ExperityBase, close_other_windows, run_logic_for_each_month
from utils import file_folder
from utils.etl.report_config import REV_19_FILE_NAME

class ExtractReports:
    def __init__(self, driver, experity: ExperityBase, experity_url, experity_version, report_export_type, download_directory, time_out=300):
        self.driver = driver
        self.experity = experity
        self.experity_url = experity_url
        self.experity_version = experity_version
        self.report_export_type = report_export_type
        self.download_directory = download_directory
        self.time_out = time_out
    
    def cnt_27(self, report_name, cnt_27_from_date, cnt_27_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(cnt_27_from_date, cnt_27_to_date)
        self.experity.select_logbook_status(['All'])
        self.experity.select_financial_class(['All'])
        self.experity.select_arrival_status(['All'])
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def cnt_19(self, report_name, cnt_19_from_date, cnt_19_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(cnt_19_from_date, cnt_19_to_date)
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def fin_25(self, report_name, fin_25_from_date, fin_25_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(fin_25_from_date, fin_25_to_date)
        self.experity.select_logbook_status(['All'])
        self.experity.select_financial_class(['All'])
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def adj_11(self, report_name, adj_11_from_date, adj_11_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(adj_11_from_date, adj_11_to_date)
        self.experity.uncheck_all_check_all("freeunReasonCodescheckall", "freeReasonCodescheck2")
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def fin_18(self, report_name, fin_18_from_date, fin_18_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(fin_18_from_date, fin_18_to_date)
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def pay_41(self, report_name, pay_41_from_date, pay_41_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(pay_41_from_date, pay_41_to_date)
        self.experity.uncheck_all_check_all("freeunPaymentReasoncheckall", "freePaymentReasoncheck1")
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def pat_2(self, report_name, pay_41_from_date, pay_41_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(pay_41_from_date, pay_41_to_date)
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def lab_01(self, report_name, pay_41_from_date, pay_41_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(pay_41_from_date, pay_41_to_date)
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def xry_03(self, report_name, xry_03_from_date, xry_03_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(xry_03_from_date, xry_03_to_date)
        self.experity.uncheck_all_check_all("freeunClinicListcheckall", "freeClinicListcheck1")
        self.experity.include_x_rays_reviewed()
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def cht_02(self, report_name, cht_02_from_date, cht_02_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(cht_02_from_date, cht_02_to_date)
        self.experity.uncheck_all_check_all("freeunClinicListcheckall", "freeClinicListcheck1")
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def med_01(self, report_name, med_01_from_date, med_01_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(med_01_from_date, med_01_to_date)
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def per_02(self, report_name, per_02_from_date, per_02_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(per_02_from_date, per_02_to_date)
        self.experity.uncheck_all_check_all("freeunPhyListcheckall", "freePhyListcheck1")
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def pat_20(self, report_name, pat_20_from_date, pat_20_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(pat_20_from_date, pat_20_to_date)
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def ccr_02(self, report_name, ccr_02_from_date, ccr_02_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(ccr_02_from_date, ccr_02_to_date)
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def ccr_03(self, report_name, ccr_03_from_date, ccr_03_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(ccr_03_from_date, ccr_03_to_date)
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def rev_16(self, report_name, rev_16_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        try:
             # Convert the input date string to a datetime object
            input_date = datetime.strptime(rev_16_date, "%Y/%m/%d")

            # Format the datetime object as "Month Year"
            formatted_date = input_date.strftime("%B %Y")
            self.experity.select_month(month = formatted_date)
        except ValueError:
            print("Invalid date format. Please provide a valid YYYY/MM/DD date.")
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def pay_4(self, report_name, pay_4_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        try:
             # Convert the input date string to a datetime object
            input_date = datetime.strptime(pay_4_date, "%Y/%m/%d")

            # Format the datetime object as "Month Year"
            formatted_date = input_date.strftime("%B %Y")
            self.experity.select_month(month = formatted_date)
        except ValueError:
            print("Invalid date format. Please provide a valid YYYY/MM/DD date.")
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def adj_4(self, report_name, adj_4_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        try:
             # Convert the input date string to a datetime object
            input_date = datetime.strptime(adj_4_date, "%Y/%m/%d")

            # Format the datetime object as "Month Year"
            formatted_date = input_date.strftime("%B %Y")
            self.experity.select_month(month = formatted_date)
        except ValueError:
            print("Invalid date format. Please provide a valid YYYY/MM/DD date.")
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def pay_10(self, report_name, pay_10_from_date, pay_10_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(pay_10_from_date, pay_10_to_date)
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def rev_19(self, report_name, rev_19_from_month, rev_19_to_month):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)

        def rev_19_report_steps(month_name):
            self.experity.select_month(month = month_name)
            self.experity.run_report()
            self.experity.download_report(self.report_export_type)
            file_folder.wait_for_download(report_name, self.download_directory)
            old_file_name = os.path.join(self.download_directory, REV_19_FILE_NAME)
            new_file_name = os.path.join(self.download_directory, f'{report_name}_{month_name}.csv')
            file_folder.rename_file_or_folder(old_file_name, new_file_name)
            close_other_windows(self.driver)

        run_logic_for_each_month(rev_19_from_month, rev_19_to_month, rev_19_report_steps)
