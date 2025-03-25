from download_reports_sequential_class import execute_report_functions

mode = "include"
report_list = ["CNT_27"]

function_args = {
    "CNT_27": {"from_date": "01/01/2025", "to_date": "03/10/2025"},
    # "CNT_19": {"from_date": "01/18/2025", "to_date": "03/07/2025"},
    # "ADJ_11": {"from_date": "01/01/2025", "to_date": "03/10/2025"},
    # "FIN_18": {"from_date": "01/18/2025", "to_date": "03/07/2025"},
    # "PAY_41": {"from_date": "01/01/2025", "to_date": "03/10/2025"},
    # "PAY_10": {"from_date": "01/17/2025", "to_date": "03/07/2025"},
    # "XRY_03": {"from_date": "01/18/2025", "to_date": "03/07/2025"},
    # "PAY_41": {"from_date": "01/01/2025", "to_date": "03/10/2025"},
    # "CCR_2": {"from_date": "01/18/2025", "to_date": "03/07/2025"},
    # "CCR_03": {"from_date": "01/01/2025", "to_date": "03/10/2025"},
    # "PER_02": {"from_date": "01/18/2025", "to_date": "03/07/2025"},
    # "MED_01": {"from_date": "01/01/2025", "to_date": "03/10/2025"},
    # "PAT_20": {"from_date": "01/18/2025", "to_date": "03/07/2025"},
    # "LAB_01": {"from_date": "01/18/2025", "to_date": "03/07/2025"},
    # "CHT_02": {"from_date": "01/01/2025", "to_date": "03/10/2025"},
    # "PAT_02": {"from_date": "01/18/2025", "to_date": "03/07/2025"},
}

execute_report_functions(mode, report_list, function_args=function_args)
