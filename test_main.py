from download_reports import execute_report_functions
from utils.report_date import get_past_date
from utils.etl.report_config import CURRENT_DATE

mode = "exclude"
# report_list = ["CNT_19", "FIN_18", "CNT_27", "ADJ_11", "PAY_41", "PAT_02"]
# report_list = ["PAT_20", "CCR_03", "PAY_10", "PAT_02", "CCR_02"]
# report_list = ["ADJ_04", "PAY_04", "REV_16"]
report_list = ["CCR_02"]

function_args = {
    "CNT_27": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "CNT_19": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "ADJ_11": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "FIN_18": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "PAY_41": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "PAY_10": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "XRY_03": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "CCR_02": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "CCR_03": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "PER_02": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "MED_01": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "PAT_20": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "LAB_01": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "CHT_02": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "PAT_02": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "ADJ_04": {"from_month": "January 2022", "to_month": "March 2025"},
    "PAY_04": {"from_month": "January 2025", "to_month": "March 2025"},
    "REV_16": {"from_month": "January 2022", "to_month": "March 2025"}
}

client_id = 3622
execute_report_functions(client_id, mode, report_list, function_args=function_args)
