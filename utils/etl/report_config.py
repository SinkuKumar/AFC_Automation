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

# Experity Configuration
EXPERITY_URL = "https://pvpm.practicevelocity.com"

# SQL Queries
CREDENTIALS_QUERY = "SELECT client_id, client_name, username, password FROM AFC_Password_Tbl WHERE active = 1 AND Client_ID IN ({client_id})"

## Report Configuration
# CNT_27 Configuration
CNT_27_REPORT_NAME = "CNT_27"
CNT_27_FROM_DATE = "01/01/2022"
CNT_27_TO_DATE = "03/17/2025"

# CNT_19 Configuration
CNT_19_REPORT_NAME = "CNT_19"
CNT_19_FROM_DATE = "01/01/2022"
CNT_19_TO_DATE = "03/17/2025"

# FIN_25 Configuration
FIN_25_REPORT_NAME = "FIN_25"
FIN_25_FROM_DATE = "01/01/2022"
FIN_25_TO_DATE = "03/17/2025"

# ADJ_11 Configuration
ADJ_11_REPORT_NAME = "ADJ_11"
ADJ_11_FROM_DATE = "01/01/2022"
ADJ_11_TO_DATE = "03/17/2025"

# FIN_18 Configuration
FIN_18_REPORT_NAME = "FIN_18"
FIN_18_FROM_DATE = "01/01/2022"
FIN_18_TO_DATE = "03/17/2025"

# PAY_41 Configuration
PAY_41_REPORT_NAME = "PAY_41"
PAY_41_FROM_DATE = "01/01/2022"
PAY_41_TO_DATE = "03/17/2025"

# PAT_2 Configuration
PAT_2_REPORT_NAME = "PAT_2"
PAT_2_FROM_DATE = "01/01/2022"
PAT_2_TO_DATE = "03/17/2025"

# LAB_01 Configuration
LAB_1_REPORT_NAME = "LAB_01"
LAB_1_FROM_DATE = "01/01/2022"
LAB_1_TO_DATE = "03/17/2025"

# XRY_03 Configuration
XRY_3_REPORT_NAME = "XRY_03"
XRY_3_FROM_DATE = "01/01/2022"
XRY_3_TO_DATE = "03/17/2025"

# CHT_02 Configuration
CHT_2_REPORT_NAME = "CHT_02"
CHT_2_FROM_DATE = "01/01/2022"
CHT_2_TO_DATE = "03/17/2025"

# MED_01 Configuration
MED_1_REPORT_NAME = "MED_01"
MED_1_FROM_DATE = "01/01/2022"
MED_1_TO_DATE = "03/17/2025"

# PER_02 Configuration
PER_2_REPORT_NAME = "PER_02"
PER_2_FROM_DATE = "01/01/2022"
PER_2_TO_DATE = "03/17/2025"

# PAT_20 Configuration
PAT_20_REPORT_NAME = "PAT_20"
PAT_20_FROM_DATE = "01/01/2022"
PAT_20_TO_DATE = "03/17/2025"

# CCR_02 Configuration
CCR_2_REPORT_NAME = "CCR_02"
CCR_2_FROM_DATE = "01/01/2022"
CCR_2_TO_DATE = "03/17/2025"

# CCR_03 Configuration
CCR_3_REPORT_NAME = "CCR_03"
CCR_3_FROM_DATE = "01/01/2022"
CCR_3_TO_DATE = "03/17/2025"

# REV_16 Configuration
REV_16_REPORT_NAME = "REV_16"
REV_16_FROM_DATE = "01/01/2022"
REV_16_TO_DATE = "03/17/2025"

# PAY_4 Configuration
PAY_4_REPORT_NAME = "PAY_4"
PAY_4_FROM_DATE = "01/01/2022"
PAY_4_TO_DATE = "03/17/2025"

# ADJ_4 Configuration
ADJ_4_REPORT_NAME = "ADJ_4"
ADJ_4_FROM_DATE = "01/01/2022"
ADJ_4_TO_DATE = "03/17/2025"

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
            "file_name": "ADJ_11_AdjustmentReport.csv",
            "base_table": "ADJ_11_Staging_Base",
            "staging_table": f"ADJ_11_Staging_{self.client_id}",
            "processed_file": f"ADJ_11_Processed_{ADJ_11_FROM_DATE.replace('/', '-')}_{ADJ_11_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

if __name__ == "__main__":
    rep_cfg = ReportConfig(3622)
    print(rep_cfg.cnt_27()['processed_file'])