import os
from datetime import datetime
import traceback
from dotenv import load_dotenv

from any_report_download import complete_report, get_logger_name

load_dotenv('utils/.env')

today = datetime.now().strftime("%Y_%m_%d")

browser = "chrome"

# TODO: remove this in production
user_info = {}
user_info['client_id'] = os.getenv("CLIENT_ID")
user_info["username"] = os.getenv('EXP_USERNAME')
user_info["password"] = os.getenv('PASSWORD')

from_date, to_date = '02/02/2025', '02/02/2025'

logger_inst = get_logger_name("report_dwnld")

report_names_staging_tables = {
    "CNT 27" : f"CNT_27_Temp_MTD_{user_info['client_id']}",
    "FIN 18" : f"FIN_18_Temp_MTD_{user_info['client_id']}",
    "ADJ 11" : f"ADJ_11_Temp_MTD_{user_info['client_id']}",
    "PAY 41" : f"PAY_11_Temp_MTD_{user_info['client_id']}",
    "CNT 19" : "CNT_19_Temp_MTD"
}

report_info ={}
report_info['download_dir'] = os.path.join(os.getcwd(), 'Downloaded Reports', today)

for report_name, staging_table in report_names_staging_tables.items():
    report_info['report_name'] = report_name
    print(report_name, staging_table)

    complete_report(staging_table_name = report_names_staging_tables[report_info['report_name']],
                    report_info = report_info,
                    user_info = user_info,
                    browser = browser,
                    from_date = from_date,
                    to_date = to_date,
                    logger_instance=logger_inst,
                    run_sp = True
                    )
