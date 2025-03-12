from datetime import datetime
# from cnt_27 import download_report, get_logger_name
import cnt_27, fin_18, cnt_19

from utils.sql_operations import MSSQLDatabase

cnt_27_start_date = "01/01/2025"
cnt_27_end_date = datetime.now().strftime("%m/%d/%Y")
fin_18_start_date = "01/01/2025"
fin_18_end_date = datetime.now().strftime("%m/%d/%Y")
cnt_19_from_date = '01/01/2025'
cnt_19_end_date = datetime.now().strftime("%m/%d/%Y")
'''
The structure of report_details and user details are present in the
`reportDetailsAndUserDetailsStructures.js` file.
'''
# report_info ={}
# report_info['report_names'] = {
#     # "ADJ_11" : [start_date, start_date],
#     # 'FIN_18' : [start_date, start_date],
#     # "CNT_27" : [start_date, start_date],
#     # "PAY_41" : [start_date, start_date],
#     # "PAT_2" : [start_date, start_date],
#     "CNT_19" : [cnt_27_start_date, cnt_27_start_date]
#     }
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
sql = MSSQLDatabase()
results = sql.execute_query("SELECT client_id, username, password FROM AFC_Password_Tbl WHERE Active = 1")
specific_clients = [3681, 3671, 16]
user_details = {}

for result in results:
    client_id, username, password = result
    if client_id in specific_clients:
        user_details[client_id] = [username, password]

logger_inst = cnt_27.get_logger_name("mtd_reports")

for specific_client in specific_clients:
    cnt_27.download_report(specific_client = specific_client, 
                           user_details = user_details,
                           browser = browser_name,
                           cnt_27_from_date = cnt_27_start_date,
                           cnt_27_to_date = cnt_27_end_date,
                           logger_instance=logger_inst,
                           run_sp=True
                           )
    fin_18.download_report(specific_client = specific_client, 
                           user_details = user_details,
                           browser = browser_name,
                           fin_18_from_date = fin_18_start_date,
                           fin_18_to_date = fin_18_end_date,
                           logger_instance=logger_inst,
                           run_sp=True
                           )

    cnt_19.download_report(specific_client = specific_client,
                           user_details = user_details,
                           browser = browser_name,
                           cnt_19_from_date = cnt_19_from_date,
                           cnt_19_to_date = cnt_19_end_date,
                           logger_instance = logger_inst,
                           run_sp = True
                           )

print("=x="*16)
print("Process Completed, Please check the email or logs.")
print("=x="*16)
