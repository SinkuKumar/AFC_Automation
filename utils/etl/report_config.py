import os
import time
from utils.general import get_past_date

# Browser Configuration
TIME_OUT = 900
BROWSER = 'chrome'
C_DIR = os.getcwd()
EXPORT_TYPE = 'CSV'
DWLD_DIR = os.path.join(C_DIR, "downloads")

# Logging Configuration
LOG_DIR = os.path.join(C_DIR, "logs/")

# Date and Time Configuration
DATE_TIME_STAMP = time.strftime("%Y-%m-%d %H:%M:%S")
DATE_STAMP = DATE_TIME_STAMP.split()[0]
TIME_STAMP = DATE_TIME_STAMP.split()[1]
CURRENT_DATE = time.strftime("%m/%d/%Y")
LOG_DT_STAMP = DATE_STAMP.replace(' ', '_').replace(':', '-')

# TODO: Apply proper dates in production
# CURRENT_DATE = '01/31/2024'


# Experity Configuration
EXPERITY_URL = "https://pvpm.practicevelocity.com"

# SQL Queries
CREDENTIALS_QUERY = "SELECT client_id, client_name, username, password FROM BI_AFC..AFC_Password_Tbl WHERE active = 1 AND Client_ID IN ({client_id})"


# PAY_4 Configuration
PAY_4_FILE_NAME = "PAY_4_TotalPaymentByDetail.csv"

# ADJ_4 Configuration
ADJ_4_FILE_NAME = "ADJ_4_AdjustmentDetail.csv"

# REV_19 Configuration
REV_19_FILE_NAME = "REV_19_TotalRevenueByProviderAndCategory.csv"

class ReportConfig:
    def __init__(self, client_id: int) -> None:
        self.client_id = client_id

    def cnt_27(self, from_date, to_date) -> dict:
        return {
            "report_name": "CNT_27",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "CNT_27_LogBookVisits.csv",
            "base_table": "CNT_27_Staging_Base",
            "staging_table": f"CNT_27_Staging_{self.client_id}",
            "raw_file":f"CNT_27_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"CNT_27_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def cnt_19(self, from_date, to_date) -> dict:
        return {
            "report_name": "CNT_19",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "CNT_19_VisitCountByCategory.csv",
            "base_table": "CNT_19_Staging_Base",
            "staging_table": f"CNT_19_Staging_{self.client_id}",
            "raw_file":f"CNT_19_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"CNT_19_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def fin_25(self, from_date, to_date) -> dict:
        return {
            "report_name": "FIN_25",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "FIN_25_RealTimeChargesReview.csv",
            "base_table": "FIN_25_Staging_Base",
            "staging_table": f"FIN_25_Staging_{self.client_id}",
            "raw_file":f"FIN_25_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"FIN_25_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def adj_11(self, from_date, to_date) -> dict:
        return {
            "report_name": "ADJ_11",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "ADJ_11_AdjustmentDetail.csv",
            "base_table": "ADJ_11_Staging_Base",
            "staging_table": f"ADJ_11_Staging_{self.client_id}",
            "raw_file":f"ADJ_11_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"ADJ_11_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def fin_18(self, from_date, to_date) -> dict:
        return {
            "report_name": "FIN_18",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "FIN_18_RebillsBySvcDate.csv",
            "base_table": "FIN_18_Staging_Base",
            "staging_table": f"FIN_18_Staging_{self.client_id}",
            "raw_file":f"FIN_18_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"FIN_18_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def pay_41(self, from_date, to_date) -> dict:
        return {
            "report_name": "PAY_41",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "PAY_41_TotalPaymentByDetail.csv",
            "base_table": "PAY_41_Staging_Base",
            "staging_table": f"PAY_41_Staging_{self.client_id}",
            "raw_file":f"PAY_41_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"PAY_41_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def pat_2(self, from_date, to_date) -> dict:
        return {
            "report_name": "PAT_2",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "PAT_2_PatientDemographicsByPractice.csv",
            "base_table": "PAT_2_Staging_Base",
            "staging_table": f"PAT_2_Staging_{self.client_id}",
            "raw_file":f"PAT_2_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"PAT_2_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def lab_01(self, from_date, to_date) -> dict:
        return {
            "report_name": "LAB_01",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "LAB_01_LabsOrdered.csv",
            "base_table": "LAB_01_Staging_Base",
            "staging_table": f"LAB_01_Staging_{self.client_id}",
            "raw_file":f"LAB_01_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"LAB_01_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def xry_03(self, from_date, to_date) -> dict:
        return {
            "report_name": "XRY_03",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "XRY_03_XRaysWaitingForReview.csv",
            "base_table": "XRY_03_Staging_Base",
            "staging_table": f"XRY_03_Staging_{self.client_id}",
            "raw_file":f"XRY_03_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"XRY_03_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def cht_02(self, from_date, to_date) -> dict:
        return {
            "report_name": "CHT_02",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "CHT_02_ChartAudit.csv",
            "base_table": "CHT_02_Staging_Base",
            "staging_table": f"CHT_02_Staging_{self.client_id}",
            "raw_file":f"CHT_02_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"CHT_02_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def med_01(self, from_date, to_date) -> dict:
        return {
            "report_name": "MED_01",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "MED_01_MedicationsByDischargingProvider.csv",
            "base_table": "MED_01_Staging_Base",
            "staging_table": f"MED_01_Staging_{self.client_id}",
            "raw_file":f"MED_01_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"MED_01_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def per_2(self, from_date, to_date) -> dict:
        return {
            "report_name": "PER_2",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "PER_2_TimeFromRegistrationToVitalsToDischarge.csv",
            "base_table": "PER_2_Staging_Base",
            "staging_table": f"PER_2_Staging_{self.client_id}",
            "raw_file":f"PER_2_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"PER_2_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def pat_20(self, from_date, to_date) -> dict:
        return {
            "report_name": "PAT_20",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "PAT_20_PatContactByProvider.csv",
            "base_table": "PAT_20_Staging_Base",
            "staging_table": f"PAT_20_Staging_{self.client_id}",
            "raw_file":f"PAT_20_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"PAT_20_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def ccr_2(self, from_date, to_date) -> dict:
        return {
            "report_name": "CCR_2",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "CCR_02_CreditCardOnFilePayments.csv",
            "base_table": "CCR_02_Staging_Base",
            "staging_table": f"CCR_02_Staging_{self.client_id}",
            "raw_file":f"CCR_02_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"CCR_2_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def ccr_3(self, from_date, to_date) -> dict:
        return {
            "report_name": "CCR_3",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "CCR_03_AllCCReserveAmounts.csv",
            "base_table": "CCR_03_Staging_Base",
            "staging_table": f"CCR_03_Staging_{self.client_id}",
            "raw_file":f"CCR_03_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"CCR_3_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def rev_16(self, from_date, to_date) -> dict:
        return {
            "report_name": "REV_16",
            "from_month": from_date,
            "to_month": from_date,
            "rev_16_date": from_date,
            "file_name": "REV_16_revenueByClinicWithDetails.csv",
            "base_table": "REV_16_Staging_Base",
            "staging_table": f"REV_16_Staging_{self.client_id}",
            "raw_file":f"REV_16_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"REV_16_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def pay_4(self, from_date, to_date) -> dict:
        return {
            "report_name": "PAY_4",
            "from_date": from_date,
            "to_date": to_date,
            "pay_4_date": from_date,
            "file_name": "PAY_4_TotalPaymentByDetail.csv",
            "base_table": "PAY_4_Staging_Base",
            "staging_table": f"PAY_4_Staging_{self.client_id}",
            "raw_file":f"PAY_4_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"PAY_4_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def adj_4(self, from_month, to_month) -> dict:
        return {
            "report_name": "ADJ_4",
            "from_month": from_month,
            "to_month": to_month,
            "file_name": "ADJ_4_AdjustmentDetail.csv",
            "base_table": "ADJ_4_Staging_Base",
            "staging_table": f"ADJ_4_Staging_{self.client_id}",
            "raw_file":f"ADJ_4_Raw_{from_month.replace(' ', '-')}_{to_month.replace(' ', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"ADJ_4_Processed_{from_month.replace(' ', '-')}_{to_month.replace(' ', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def pay_10(self, from_date, to_date) -> dict:
        return {
            "report_name": "PAY_10",
            "from_date": from_date,
            "to_date": to_date,
            "file_name": "PAY_10_PayerPatientPaidAdjustedByPayerClass.csv",
            "base_table": "PAY_10_Staging_Base",
            "staging_table": f"PAY_10_Staging_{self.client_id}",
            "raw_file":f"PAY_10_Raw_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"PAY_10_Processed_{from_date.replace('/', '-')}_{to_date.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

    def rev_19(self, from_month, to_month) -> dict:
        return {
            "report_name": "REV_19",
            "from_month": from_month,
            "to_month": to_month,
            "file_name": "REV_19_TotalRevenueByProviderAndCategory.csv",
            "base_table": "REV_19_Staging_Base",
            "staging_table": f"REV_19_Staging_{self.client_id}",
            "raw_file":f"REV_19_Raw_{from_month.replace(' ', '-')}_{to_month.replace(' ', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
            "processed_file": f"REV_19_Processed_{from_month.replace(' ', '-')}_{to_month.replace(' ', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }


if __name__ == "__main__":
    rep_cfg = ReportConfig(3622)
    print(rep_cfg.cnt_27()['processed_file'])