import os
import time

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

## Report Configuration
# CNT_27 Configuration
CNT_27_REPORT_NAME = "CNT_27"
CNT_27_FROM_DATE = "01/01/2024"
CNT_27_TO_DATE = CURRENT_DATE

# CNT_19 Configuration
CNT_19_REPORT_NAME = "CNT_19"
CNT_19_FROM_DATE = "01/01/2024"
CNT_19_TO_DATE = CURRENT_DATE

# FIN_25 Configuration
FIN_25_REPORT_NAME = "FIN_25"
FIN_25_FROM_DATE = "02/01/2025"
FIN_25_TO_DATE = CURRENT_DATE

# ADJ_11 Configuration
ADJ_11_REPORT_NAME = "ADJ_11"
ADJ_11_FROM_DATE = "01/01/2024"
ADJ_11_TO_DATE = CURRENT_DATE

# FIN_18 Configuration
FIN_18_REPORT_NAME = "FIN_18"
FIN_18_FROM_DATE = "01/01/2024"
FIN_18_TO_DATE = CURRENT_DATE

# PAY_41 Configuration
PAY_41_REPORT_NAME = "PAY_41"
PAY_41_FROM_DATE = "01/01/2024"
PAY_41_TO_DATE = CURRENT_DATE

# PAT_2 Configuration
PAT_2_REPORT_NAME = "PAT_2"
PAT_2_FROM_DATE = "01/01/2025"
PAT_2_TO_DATE = CURRENT_DATE

# LAB_01 Configuration
LAB_01_REPORT_NAME = "LAB_01"
LAB_01_FROM_DATE = "01/01/2025"
LAB_01_TO_DATE = CURRENT_DATE

# XRY_03 Configuration
XRY_03_REPORT_NAME = "XRY_03"
XRY_03_FROM_DATE = "01/01/2024"
XRY_03_TO_DATE = CURRENT_DATE

# CHT_02 Configuration
CHT_02_REPORT_NAME = "CHT_02"
CHT_02_FROM_DATE = "01/01/2025"
CHT_02_TO_DATE = CURRENT_DATE

# MED_01 Configuration
MED_01_REPORT_NAME = "MED_01"
MED_01_FROM_DATE = "01/01/2025"
MED_01_TO_DATE = CURRENT_DATE

# PER_02 Configuration
PER_2_REPORT_NAME = "PER_02"
PER_2_FROM_DATE = "01/01/2024"
PER_2_TO_DATE = CURRENT_DATE

# PAT_20 Configuration
PAT_20_REPORT_NAME = "PAT_20"
PAT_20_FROM_DATE = "01/01/2024"
PAT_20_TO_DATE = CURRENT_DATE

# CCR_02 Configuration
CCR_2_REPORT_NAME = "CCR_02"
CCR_2_FROM_DATE = "01/01/2024"
CCR_2_TO_DATE = CURRENT_DATE

# CCR_03 Configuration
CCR_3_REPORT_NAME = "CCR_03"
CCR_3_FROM_DATE = "01/01/2024"
CCR_3_TO_DATE = CURRENT_DATE

# REV_16 Configuration
REV_16_REPORT_NAME = "REV_16"
REV_16_FROM_DATE = "01/01/2024"
REV_16_TO_DATE = CURRENT_DATE

# PAY_4 Configuration
PAY_4_REPORT_NAME = "PAY_4"
PAY_4_FROM_DATE = "01/01/2024"
PAY_4_TO_DATE = CURRENT_DATE

# ADJ_4 Configuration
ADJ_4_REPORT_NAME = "ADJ_4"
ADJ_4_FROM_DATE = "01/01/2024"
ADJ_4_TO_DATE = CURRENT_DATE

# PAY_10 Configuration
PAY_10_REPORT_NAME = "PAY_10"
PAY_10_FROM_DATE = "12/01/2024"
PAY_10_TO_DATE = CURRENT_DATE

# REV_19 Configuration
REV_19_REPORT_NAME = "REV_19"
REV_19_FROM_MONTH = "January 2025"
REV_19_TO_MONTH = "February 2025"
REV_19_FILE_NAME = "REV_19_TotalRevenueByProviderAndCategory.csv"
## TODO: Add these reports as well
# PCD_31 Configuration
PCD_31_REPORT_NAME = "PCD_31"
PCD_31_FROM_DATE = "01/01/2024"
PCD_31_TO_DATE = CURRENT_DATE

# PAY_6 Configuration
PAY_6_REPORT_NAME = "PAY_6"
PAY_6_FROM_DATE = "01/01/2024"
PAY_6_TO_DATE = CURRENT_DATE

class ReportConfig:
    def __init__(self, client_id: int) -> None:
        self.client_id = client_id

    def cnt_27(self) -> dict:
        return {
            "report_name": CNT_27_REPORT_NAME,
            "from_date": CNT_27_FROM_DATE,
            "to_date": CNT_27_TO_DATE,
            "file_name": "CNT_27_LogBookVisits.csv",
            "base_table": "CNT_27_Staging_Base",
            "staging_table": f"CNT_27_Staging_{self.client_id}",
            "processed_file": f"CNT_27_Processed_{CNT_27_FROM_DATE.replace('/', '-')}_{CNT_27_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def cnt_19(self) -> dict:
        return {
            "report_name": CNT_19_REPORT_NAME,
            "from_date": CNT_19_FROM_DATE,
            "to_date": CNT_19_TO_DATE,
            "file_name": "CNT_19_VisitCountByCategory.csv",
            "base_table": "CNT_19_Staging_Base",
            "staging_table": f"CNT_19_Staging_{self.client_id}",
            "processed_file": f"CNT_19_Processed_{CNT_19_FROM_DATE.replace('/', '-')}_{CNT_19_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def fin_25(self) -> dict:
        return {
            "report_name": FIN_25_REPORT_NAME,
            "from_date": FIN_25_FROM_DATE,
            "to_date": FIN_25_TO_DATE,
            "file_name": "FIN_25_RealTimeChargesReview.csv",
            "base_table": "FIN_25_Staging_Base",
            "staging_table": f"FIN_25_Staging_{self.client_id}",
            "processed_file": f"FIN_25_Processed_{FIN_25_FROM_DATE.replace('/', '-')}_{FIN_25_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def adj_11(self) -> dict:
        return {
            "report_name": ADJ_11_REPORT_NAME,
            "from_date": ADJ_11_FROM_DATE,
            "to_date": ADJ_11_TO_DATE,
            "file_name": "ADJ_11_AdjustmentDetail.csv",
            "base_table": "ADJ_11_Staging_Base",
            "staging_table": f"ADJ_11_Staging_{self.client_id}",
            "processed_file": f"ADJ_11_Processed_{ADJ_11_FROM_DATE.replace('/', '-')}_{ADJ_11_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def fin_18(self) -> dict:
        return {
            "report_name": FIN_18_REPORT_NAME,
            "from_date": FIN_18_FROM_DATE,
            "to_date": FIN_18_TO_DATE,
            "file_name": "FIN_18_RebillsBySvcDate.csv",
            "base_table": "FIN_18_Staging_Base",
            "staging_table": f"FIN_18_Staging_{self.client_id}",
            "processed_file": f"FIN_18_Processed_{FIN_18_FROM_DATE.replace('/', '-')}_{FIN_18_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def pay_41(self) -> dict:
        return {
            "report_name": PAY_41_REPORT_NAME,
            "from_date": PAY_41_FROM_DATE,
            "to_date": PAY_41_TO_DATE,
            "file_name": "PAY_41_TotalPaymentByDetail.csv",
            "base_table": "PAY_41_Staging_Base",
            "staging_table": f"PAY_41_Staging_{self.client_id}",
            "processed_file": f"PAY_41_Processed_{PAY_41_FROM_DATE.replace('/', '-')}_{PAY_41_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def pat_2(self) -> dict:
        return {
            "report_name": PAT_2_REPORT_NAME,
            "from_date": PAT_2_FROM_DATE,
            "to_date": PAT_2_TO_DATE,
            "file_name": "PAT_2_PatientDemographicsByPractice.csv",
            "base_table": "PAT_2_Staging_Base",
            "staging_table": f"PAT_2_Staging_{self.client_id}",
            "processed_file": f"PAT_2_Processed_{PAT_2_FROM_DATE.replace('/', '-')}_{PAT_2_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def lab_01(self) -> dict:
        return {
            "report_name": LAB_01_REPORT_NAME,
            "from_date": LAB_01_FROM_DATE,
            "to_date": LAB_01_TO_DATE,
            "file_name": "LAB_01_LabsOrdered.csv",
            "base_table": "LAB_01_Staging_Base",
            "staging_table": f"LAB_01_Staging_{self.client_id}",
            "processed_file": f"LAB_01_Processed_{LAB_01_FROM_DATE.replace('/', '-')}_{LAB_01_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def xry_03(self) -> dict:
        return {
            "report_name": XRY_03_REPORT_NAME,
            "from_date": XRY_03_FROM_DATE,
            "to_date": XRY_03_TO_DATE,
            "file_name": "XRY_03_XRaysWaitingForReview.csv",
            "base_table": "XRY_03_Staging_Base",
            "staging_table": f"XRY_03_Staging_{self.client_id}",
            "processed_file": f"XRY_03_Processed_{XRY_03_FROM_DATE.replace('/', '-')}_{XRY_03_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def cht_02(self) -> dict:
        return {
            "report_name": CHT_02_REPORT_NAME,
            "from_date": CHT_02_FROM_DATE,
            "to_date": CHT_02_TO_DATE,
            "file_name": "CHT_02_ChartAudit.csv",
            "base_table": "CHT_02_Staging_Base",
            "staging_table": f"CHT_02_Staging_{self.client_id}",
            "processed_file": f"CHT_02_Processed_{CHT_02_FROM_DATE.replace('/', '-')}_{CHT_02_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def med_01(self) -> dict:
        return {
            "report_name": MED_01_REPORT_NAME,
            "from_date": MED_01_FROM_DATE,
            "to_date": MED_01_TO_DATE,
            "file_name": "MED_01_MedicationsByDischargingProvider.csv",
            "base_table": "MED_01_Staging_Base",
            "staging_table": f"MED_01_Staging_{self.client_id}",
            "processed_file": f"MED_01_Processed_{MED_01_FROM_DATE.replace('/', '-')}_{MED_01_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def per_2(self) -> dict:
        return {
            "report_name": PER_2_REPORT_NAME,
            "from_date": PER_2_FROM_DATE,
            "to_date": PER_2_TO_DATE,
            "file_name": "PER_2_TimeFromRegistrationToVitalsToDischarge.csv",
            "base_table": "PER_2_Staging_Base",
            "staging_table": f"PER_2_Staging_{self.client_id}",
            "processed_file": f"PER_2_Processed_{PER_2_FROM_DATE.replace('/', '-')}_{PER_2_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def pat_20(self) -> dict:
        return {
            "report_name": PAT_20_REPORT_NAME,
            "from_date": PAT_20_FROM_DATE,
            "to_date": PAT_20_TO_DATE,
            "file_name": "PAT_20_PatContactByProvider.csv",
            "base_table": "PAT_20_Staging_Base",
            "staging_table": f"PAT_20_Staging_{self.client_id}",
            "processed_file": f"PAT_20_Processed_{PAT_20_FROM_DATE.replace('/', '-')}_{PAT_20_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def ccr_2(self) -> dict:
        return {
            "report_name": CCR_2_REPORT_NAME,
            "from_date": CCR_2_FROM_DATE,
            "to_date": CCR_2_TO_DATE,
            "file_name": "CCR_02_CreditCardOnFilePayments.csv",
            "base_table": "CCR_02_Staging_Base",
            "staging_table": f"CCR_2_Staging_{self.client_id}",
            "processed_file": f"CCR_2_Processed_{CCR_2_FROM_DATE.replace('/', '-')}_{CCR_2_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def ccr_3(self) -> dict:
        return {
            "report_name": CCR_3_REPORT_NAME,
            "from_date": CCR_3_FROM_DATE,
            "to_date": CCR_3_TO_DATE,
            "file_name": "CCR_03_AllCCReserveAmounts.csv",
            "base_table": "CCR_03_Staging_Base",
            "staging_table": f"CCR_3_Staging_{self.client_id}",
            "processed_file": f"CCR_3_Processed_{CCR_3_FROM_DATE.replace('/', '-')}_{CCR_3_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def rev_16(self) -> dict:
        return {
            "report_name": REV_16_REPORT_NAME,
            "from_date": REV_16_FROM_DATE,
            "to_date": REV_16_TO_DATE,
            "file_name": "REV_16_RevenueReport.csv",
            "base_table": "REV_16_Staging_Base",
            "staging_table": f"REV_16_Staging_{self.client_id}",
            "processed_file": f"REV_16_Processed_{REV_16_FROM_DATE.replace('/', '-')}_{REV_16_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def pay_4(self) -> dict:
        return {
            "report_name": PAY_4_REPORT_NAME,
            "from_date": PAY_4_FROM_DATE,
            "to_date": PAY_4_TO_DATE,
            "file_name": "PAY_4_PaymentReport.csv",
            "base_table": "PAY_4_Staging_Base",
            "staging_table": f"PAY_4_Staging_{self.client_id}",
            "processed_file": f"PAY_4_Processed_{PAY_4_FROM_DATE.replace('/', '-')}_{PAY_4_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def adj_4(self) -> dict:
        return {
            "report_name": ADJ_4_REPORT_NAME,
            "from_date": ADJ_4_FROM_DATE,
            "to_date": ADJ_4_TO_DATE,
            "file_name": "ADJ_4_AdjustmentReport.csv",
            "base_table": "ADJ_4_Staging_Base",
            "staging_table": f"ADJ_4_Staging_{self.client_id}",
            "processed_file": f"ADJ_4_Processed_{ADJ_4_FROM_DATE.replace('/', '-')}_{ADJ_4_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def pay_10(self) -> dict:
        return {
            "report_name": PAY_10_REPORT_NAME,
            "from_date": PAY_10_FROM_DATE,
            "to_date": PAY_10_TO_DATE,
            "file_name": "PAY_10_PayerPatientPaidAdjustedByPayerClass.csv",
            "base_table": "PAY_10_Staging_Base",
            "staging_table": f"PAY_10_Staging_{self.client_id}",
            "processed_file": f"PAY_10_Processed_{PAY_10_FROM_DATE.replace('/', '-')}_{PAY_10_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }
    
    def rev_19(self) -> dict:
        return {
            "report_name": REV_19_REPORT_NAME,
            "from_month": REV_19_FROM_MONTH,
            "to_month": REV_19_TO_MONTH,
            "file_name": "REV_19_TotalRevenueByProviderAndCategory.csv",
            "base_table": "REV_19_Staging_Base",
            "staging_table": f"REV_19_Staging_{self.client_id}",
            "processed_file": f"REV_19_Processed_{REV_19_FROM_MONTH.replace(' ', '-')}_{REV_19_TO_MONTH.replace(' ', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }


if __name__ == "__main__":
    rep_cfg = ReportConfig(3622)
    print(rep_cfg.cnt_27()['processed_file'])