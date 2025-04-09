import argparse
import json
from download_reports import execute_report_functions

parser = argparse.ArgumentParser(description="Run report functions with given parameters.")

parser.add_argument('--mode', type=str, required=True)
parser.add_argument('--report_list', type=str, help='JSON list of reports, e.g. ["CNT_27"]')
parser.add_argument('--client_id', type=int, required=True)
parser.add_argument('--function_args', type=str, required=True)

args = parser.parse_args()

try:
    report_list = json.loads(args.report_list) if args.report_list else []
    function_args = json.loads(args.function_args)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON input: {e}")
    exit(1)

execute_report_functions(args.client_id, args.mode, report_list, function_args=function_args)
