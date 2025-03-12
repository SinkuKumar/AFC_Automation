import sys
import os

# Add the project's root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase, close_other_windows
from utils import file_folder

# Not an actual implementation just to make the intellisense work during development

class Reports:
    def __init__(self, driver, experity, experity_url, experity_version, report_export_type, download_directory, time_out):
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
        file_folder.wait_for_download(report_name, self.download_directory, self.time_out)
        close_other_windows(self.driver)

    def cnt_19(self, report_name, cnt_19_from_date, cnt_19_to_date):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(cnt_19_from_date, cnt_19_to_date)
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory, self.time_out)
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
