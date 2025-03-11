from datetime import datetime
# from cnt_27 import download_report, get_logger_name
import cnt_27

cnt_27_start_date = "01/01/2025"
cnt_27_end_date = datetime.now().strftime("%m/%d/%Y")
'''
The structure of report_details and user details are present in the
`reportDetailsAndUserDetailsStructures.js` file.
'''
report_info ={}
report_info['report_names'] = {
    # "ADJ_11" : [start_date, start_date],
    # 'FIN_18' : [start_date, start_date],
    # "CNT_27" : [start_date, start_date],
    # "PAY_41" : [start_date, start_date],
    # "PAT_2" : [start_date, start_date],
    "CNT_19" : [cnt_27_start_date, cnt_27_start_date]
    }
# report_details['download_dir'] = os.path.join(os.getcwd(), 'Downloaded Reports', today)

# Put the name of the required clients here.
specific_clients = [3681, 3671, 16]

browser_name = "chrome"

'''
User details is a dictionary.
The keys of user details are the client_ids.
The values are lists:
    1. the first element is username for the client
    2. the second element is password for the client
'''

logger_inst = cnt_27.get_logger_name("mtd_reports")

cnt_27.download_report(specific_client_list = specific_clients,
                browser = browser_name,
                cnt_27_from_date = cnt_27_start_date,
                cnt_27_to_date = cnt_27_end_date,
                logger_instance=logger_inst,
                run_sp=True
                )