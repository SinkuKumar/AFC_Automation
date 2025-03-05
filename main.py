import os
from datetime import datetime
import traceback
from dotenv import load_dotenv

from cnt_27_report_download import complete_report, get_logger_name

load_dotenv('.env')

today = datetime.now().strftime("%Y_%m_%d")
report_info ={}
report_info['report_name'] = "CNT_27"
report_info['download_dir'] = os.path.join(os.getcwd(), 'Downloaded Reports', today)
browser = "chrome"

# TODO: remove this in production
user_info = {}
user_info['client_id'] = os.getenv("CLIENT_ID")
user_info["username"] = os.getenv('EXP_USERNAME')
user_info["password"] = os.getenv('PASSWORD')

logger_inst = get_logger_name("main")

complete_report(report_info = report_info,
                browser = browser, user_info=user_info,
                logger_instance=logger_inst
                )
