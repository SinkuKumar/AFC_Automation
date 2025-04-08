import multiprocessing
from download_reports import execute_report_functions
from utils.report_date import get_past_date
from utils.etl.report_config import CURRENT_DATE


def run_reports_for_client(client_id):
    mode = "include"
    report_list = ["REV_16"]

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
        "REV_16": {"from_month": "January 2022", "to_month": "March 2025"},
    }

    execute_report_functions(client_id, mode, report_list, function_args=function_args)


if __name__ == "__main__":
    MAX_WORKERS = 8
    client_ids = [16, 3622, 3630, 3735, 3625, 3649, 3650, 3736, 822, 655, 3657, 640, 489, 36, 3671, 3672, 3624, 3678, 3681, 3696, 3698, 3697, 3705, 3716, 3720, 3718, 3665, 3724, 3725, 3726, 3670]
    client_ids = [3622]
    num_workers = min(MAX_WORKERS, len(client_ids))  # Set max workers to 8 or number of clients

    with multiprocessing.Pool(processes=num_workers) as pool:
        pool.map(run_reports_for_client, client_ids)
