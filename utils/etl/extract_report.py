"""
Module: extract_reports

This module provides functionality for extracting various reports using the Experity system.
It automates the navigation, selection, and downloading of different reports based on
specified date ranges or months.

Classes:
    ExtractReports: Handles extraction of multiple reports using the ExperityBase instance.

Dependencies:
    - os
    - sys
    - time
    - datetime
    - utils.experity_base
    - utils.file_folder
    - utils.etl.report_config
"""

import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils.experity_base import ExperityBase, close_other_windows, run_logic_for_each_month
from utils import file_folder
from utils.etl.report_config import REV_19_FILE_NAME, ADJ_4_FILE_NAME, PAY_4_FILE_NAME


class ExtractReports:
    """
    ExtractReports class provides methods to automate the extraction of various reports
    from the Experity platform. Each method corresponds to a specific report type and
    handles the navigation, selection, and downloading of the report.

    Attributes:
        driver: WebDriver instance used for browser automation.
        experity: An instance of ExperityBase for interacting with the Experity platform.
        experity_url: The base URL of the Experity platform.
        experity_version: The version of the Experity platform.
        report_export_type: The format in which reports are exported (e.g., CSV, PDF).
        download_directory: The directory where downloaded reports are saved.
        time_out: Maximum time to wait for downloads to complete (default is 300 seconds).

    Methods:
        cnt_27(report_name, cnt_27_from_date, cnt_27_to_date):
            Extracts the CNT_27 report for a specified date range.

        cnt_19(report_name, cnt_19_from_date, cnt_19_to_date):
            Extracts the CNT_19 report for a specified date range.

        fin_25(report_name, fin_25_from_date, fin_25_to_date):
            Extracts the FIN_25 report for a specified date range.

        adj_11(report_name, adj_11_from_date, adj_11_to_date):
            Extracts the ADJ_11 report for a specified date range.

        fin_18(report_name, fin_18_from_date, fin_18_to_date):
            Extracts the FIN_18 report for a specified date range.

        pay_41(report_name, pay_41_from_date, pay_41_to_date):
            Extracts the PAY_41 report for a specified date range.

        pat_2(report_name, pay_41_from_date, pay_41_to_date):
            Extracts the PAT_2 report for a specified date range.

        lab_01(report_name, pay_41_from_date, pay_41_to_date):
            Extracts the LAB_01 report for a specified date range.

        xry_03(report_name, xry_03_from_date, xry_03_to_date):
            Extracts the XRY_03 report for a specified date range.

        cht_02(report_name, cht_02_from_date, cht_02_to_date):
            Extracts the CHT_02 report for a specified date range.

        med_01(report_name, med_01_from_date, med_01_to_date):
            Extracts the MED_01 report for a specified date range.

        per_02(report_name, per_02_from_date, per_02_to_date):
            Extracts the PER_02 report for a specified date range.

        pat_20(report_name, pat_20_from_date, pat_20_to_date):
            Extracts the PAT_20 report for a specified date range.

        ccr_02(report_name, ccr_02_from_date, ccr_02_to_date):
            Extracts the CCR_02 report for a specified date range.

        ccr_03(report_name, ccr_03_from_date, ccr_03_to_date):
            Extracts the CCR_03 report for a specified date range.

        rev_16(report_name, rev_16_date):
            Extracts the REV_16 report for a specified month based on the provided date.

        pay_4(report_name, pay_4_from_month, pay_4_to_month):
            Extracts the PAY_4 report for each month in the specified range.

        adj_4(report_name, adj_4_from_month, adj_4_to_month):
            Extracts the ADJ_4 report for each month in the specified range.

        pay_10(report_name, pay_10_from_date, pay_10_to_date):
            Extracts the PAY_10 report for a specified date range.

        rev_19(report_name, rev_19_from_month, rev_19_to_month):
            Extracts the REV_19 report for each month in the specified range.
    """

    def __init__(self, driver, experity: ExperityBase, experity_url, experity_version, report_export_type, download_directory, time_out=300):
        """
        Initializes the ExtractReport class with the necessary parameters.
        Args:
            driver: The web driver instance used for browser automation.
            experity (ExperityBase): An instance of the ExperityBase class for interacting with Experity.
            experity_url (str): The base URL for the Experity application.
            experity_version (str): The version of the Experity application being used.
            report_export_type (str): The type of report export (e.g., CSV, PDF).
            download_directory (str): The directory where downloaded reports will be saved.
            time_out (int, optional): The maximum time (in seconds) to wait for operations to complete. Defaults to 300.
        """

        self.driver = driver
        self.experity = experity
        self.experity_url = experity_url
        self.experity_version = experity_version
        self.report_export_type = report_export_type
        self.download_directory = download_directory
        self.time_out = time_out

    def if_downloaded(self):
        """
        Check if the report is already downloaded
        """
        pass

    def cnt_27(self, report_name, cnt_27_from_date, cnt_27_to_date):
        """
        Generates and downloads a report based on the specified parameters.

        Args:
            report_name (str): The name of the report to be generated.
            cnt_27_from_date (str): The start date for the report's date range in the format 'YYYY-MM-DD'.
            cnt_27_to_date (str): The end date for the report's date range in the format 'YYYY-MM-DD'.

        Steps:
            1. Navigates to the Reports section of the Experity application.
            2. Searches for and selects the specified report.
            3. Sets the date range for the report.
            4. Configures additional filters such as logbook status, financial class, and arrival status.
            5. Runs the report and downloads it in the specified export format.
            6. Waits for the download to complete and ensures the file is saved in the designated directory.
            7. Closes any additional browser windows opened during the process.

        Raises:
            Exception: If any step in the report generation or download process fails.
        """

        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(cnt_27_from_date, cnt_27_to_date)
        self.experity.select_logbook_status(["All"])
        self.experity.select_financial_class(["All"])
        self.experity.select_arrival_status(["All"])
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def cnt_19(self, report_name, cnt_19_from_date, cnt_19_to_date):
        """
        Generates and downloads a report based on the specified date range.

        Args:
            report_name (str): The name of the report to be generated.
            cnt_19_from_date (str): The start date for the report in the format 'YYYY-MM-DD'.
            cnt_19_to_date (str): The end date for the report in the format 'YYYY-MM-DD'.

        Steps:
            1. Navigates to the "Reports" section in the Experity application.
            2. Searches for and selects the specified report.
            3. Sets the date range for the report.
            4. Runs the report.
            5. Downloads the report in the specified export format.
            6. Waits for the report to be downloaded to the specified directory.
            7. Closes any additional browser windows opened during the process.

        Raises:
            Exception: If any step in the report generation or download process fails.
        """
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(cnt_19_from_date, cnt_19_to_date)
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def fin_25(self, report_name, fin_25_from_date, fin_25_to_date):
        """
        Generates and downloads a financial report (FIN 25) from the Experity system.

        Args:
            report_name (str): The name of the report to be generated.
            fin_25_from_date (str): The start date for the report's date range in the format 'YYYY-MM-DD'.
            fin_25_to_date (str): The end date for the report's date range in the format 'YYYY-MM-DD'.

        Steps:
            1. Navigates to the Reports section of the Experity system.
            2. Searches for and selects the specified report.
            3. Sets the date range for the report.
            4. Selects "All" for logbook status and financial class filters.
            5. Runs the report and downloads it in the specified export format.
            6. Waits for the report to be downloaded to the specified directory.
            7. Closes any additional browser windows opened during the process.

        Raises:
            Exception: If the report download fails or any step encounters an error.
        """
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)
        self.experity.select_report_date_range(fin_25_from_date, fin_25_to_date)
        self.experity.select_logbook_status(["All"])
        self.experity.select_financial_class(["All"])
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
        self.experity.select_date_type("Created Date")
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
        file_folder.wait_for_download("PER_2", self.download_directory)
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
            self.experity.select_month(month=formatted_date)
        except ValueError:
            print("Invalid date format. Please provide a valid YYYY/MM/DD date.")
        self.experity.run_report()
        self.experity.download_report(self.report_export_type)
        file_folder.wait_for_download(report_name, self.download_directory)
        close_other_windows(self.driver)

    def pay_4(self, report_name, pay_4_from_month, pay_4_to_month):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)

        def pay_4_report_steps(month_name):
            self.experity.select_month(month=month_name)
            self.experity.run_report()
            self.experity.download_report(self.report_export_type)
            file_folder.wait_for_download(PAY_4_FILE_NAME, self.download_directory)
            old_file_name = os.path.join(self.download_directory, PAY_4_FILE_NAME)
            new_file_name = os.path.join(self.download_directory, f"{report_name}_{month_name}.csv")
            file_folder.rename_file_or_folder(old_file_name, new_file_name)
            with open(new_file_name, "r") as file:
                lines = file.readlines()[3:]

            with open(new_file_name, "w") as file:
                file.writelines(lines)

            close_other_windows(self.driver)

        run_logic_for_each_month(pay_4_from_month, pay_4_to_month, pay_4_report_steps)

    def adj_4(self, report_name, adj_4_from_month, adj_4_to_month):
        self.experity.navigate_to(self.experity_url, self.experity_version, "Reports")
        self.experity.search_and_select_report(report_name)

        def adj_4_report_steps(month_name):
            self.experity.select_month(month=month_name)
            self.experity.run_report()
            self.experity.download_report(self.report_export_type)
            file_folder.wait_for_download(ADJ_4_FILE_NAME, self.download_directory)
            old_file_name = os.path.join(self.download_directory, ADJ_4_FILE_NAME)
            new_file_name = os.path.join(self.download_directory, f"{report_name}_{month_name}.csv")
            file_folder.rename_file_or_folder(old_file_name, new_file_name)
            with open(new_file_name, "r") as file:
                lines = file.readlines()[3:]

            with open(new_file_name, "w") as file:
                file.writelines(lines)

            close_other_windows(self.driver)

        run_logic_for_each_month(adj_4_from_month, adj_4_to_month, adj_4_report_steps)

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
            self.experity.select_month(month=month_name)
            self.experity.run_report()
            self.experity.download_report(self.report_export_type)
            file_folder.wait_for_download(REV_19_FILE_NAME, self.download_directory)
            old_file_name = os.path.join(self.download_directory, REV_19_FILE_NAME)
            new_file_name = os.path.join(self.download_directory, f"{report_name}_{month_name}.csv")
            file_folder.rename_file_or_folder(old_file_name, new_file_name)
            close_other_windows(self.driver)

        run_logic_for_each_month(rev_19_from_month, rev_19_to_month, rev_19_report_steps)
