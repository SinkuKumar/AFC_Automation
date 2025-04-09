import argparse
import json
from download_reports import execute_report_functions
from utils.report_date import get_past_date
from utils.etl.report_config import CURRENT_DATE


# Define the default function_args dictionary
DEFAULT_FUNCTION_ARGS = {
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
    "PAY_04": {"from_month": "January 2022", "to_month": "March 2025"},
    "REV_16": {"from_month": "January 2022", "to_month": "March 2025"}
}


def main():
    parser = argparse.ArgumentParser(description="Run report generation process.")
    parser.add_argument("--client_id", type=int, required=True, help="Client ID")
    parser.add_argument("--mode", type=str, default="include", help="Mode of operation")
    parser.add_argument(
        "--report_list", type=str, required=True,
        help="Comma-separated list of report codes (e.g. 'PAY_04,PAT_02')"
    )
    parser.add_argument(
        "--function_args", type=str, default=None,
        help="Optional JSON string with report-specific arguments"
    )

    args = parser.parse_args()

    report_list = args.report_list.split(",")
    if args.function_args:
        try:
            function_args = json.loads(args.function_args)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON provided for function_args.")
    else:
        function_args = {key: DEFAULT_FUNCTION_ARGS[key] for key in report_list if key in DEFAULT_FUNCTION_ARGS}

    execute_report_functions(
        client_id=args.client_id,
        mode=args.mode,
        function_list=report_list,
        function_args=function_args
    )


if __name__ == "__main__":
    main()
