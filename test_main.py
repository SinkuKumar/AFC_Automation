from download_reports_sequential import execute_report_functions
from utils.report_date import get_past_date
from utils.etl.report_config import CURRENT_DATE

mode = "all"
report_list = ["CCR_02"]

function_args = {
    "CNT_27": {"from_date": get_past_date(days=60), "to_date": CURRENT_DATE},
    "CNT_19": {"from_date": get_past_date(days=60), "to_date": CURRENT_DATE},
    "ADJ_11": {"from_date": get_past_date(days=60), "to_date": CURRENT_DATE},
    "FIN_18": {"from_date": get_past_date(days=60), "to_date": CURRENT_DATE},
    "PAY_41": {"from_date": get_past_date(days=60), "to_date": CURRENT_DATE},
    "PAY_10": {"from_date": get_past_date(year=1), "to_date": CURRENT_DATE},
    "XRY_03": {"from_date": get_past_date(days=2), "to_date": CURRENT_DATE},
    "CCR_02": {"from_date": get_past_date(days=60), "to_date": CURRENT_DATE},
    "CCR_03": {"from_date": get_past_date(days=90), "to_date": CURRENT_DATE},
    "PER_02": {"from_date": get_past_date(days=2), "to_date": CURRENT_DATE},
    "MED_01": {"from_date": get_past_date(days=2), "to_date": CURRENT_DATE},
    "PAT_20": {"from_date": "01/01/2022", "to_date": CURRENT_DATE},
    "LAB_01": {"from_date": get_past_date(days=2), "to_date": CURRENT_DATE},
    "CHT_02": {"from_date": get_past_date(days=2), "to_date": CURRENT_DATE},
    "PAT_02": {"from_date": get_past_date(days=60), "to_date": CURRENT_DATE},
    "ADJ_04": {"from_month": "August 2024", "to_month": "February 2025"},
    "PAY_04": {"from_month": "February 2025", "to_month": "February 2025"},
    "REV_16": {"from_date": "2025/02/01", "to_date": CURRENT_DATE[-4:] + "/" + CURRENT_DATE[:2] + "/" + CURRENT_DATE[3:5]}
}

client_id = 640
execute_report_functions(client_id, mode, report_list, function_args=function_args)
