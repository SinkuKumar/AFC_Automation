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
CREDENTIALS_QUERY = "SELECT client_id, client_name, username, password FROM AFC_Password_Tbl WHERE active = 1 AND client_id in ({client_id})"

## Report Configuration
# CNT_27 Configuration
CNT_27_REPORT_NAME = "CNT_27"
CNT_27_FROM_DATE = "01/01/2022"
CNT_27_TO_DATE = "03/17/2025"

# CNT_19 Configuration
CNT_19_REPORT_NAME = "CNT_19"
CNT_19_FROM_DATE = "01/01/2022"
CNT_19_TO_DATE = "03/17/2025"

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
            "processed_file": f"CNT_19_Processed_{CNT_27_FROM_DATE.replace('/', '-')}_{CNT_27_TO_DATE.replace('/', '-')}_{TIME_STAMP.replace(':', '-')}.csv",
        }

if __name__ == "__main__":
    rep_cfg = ReportConfig(3622)
    print(rep_cfg.cnt_27()['processed_file'])